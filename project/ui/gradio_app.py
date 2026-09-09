import gradio as gr
from core.chat_interface import ChatInterface
from core.document_manager import DocumentManager
from core.rag_system import RAGSystem
import config
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

def create_gradio_ui():
    rag_system = RAGSystem()
    rag_system.initialize()
    
    doc_manager = DocumentManager(rag_system)
    chat_interface = ChatInterface(rag_system)
    
    def format_file_list():
        files = doc_manager.get_markdown_files()
        if not files:
            return "No documents indexed yet."
        return "\n".join([f"{f}" for f in files])
    
    def upload_handler(files, progress=gr.Progress()):
        if not files:
            gr.Warning("Choose a PDF or Markdown file in the box above first.")
            return None, format_file_list()

        try:
            added, skipped = doc_manager.add_documents(
                files,
                progress_callback=lambda p, desc: progress(p, desc=desc),
            )
        except Exception as exc:
            gr.Error(f"Upload failed: {exc}")
            return None, format_file_list()

        if added:
            gr.Info(f"Added {added} document(s)." + (f" Skipped {skipped} already indexed." if skipped else ""))
        elif skipped:
            gr.Warning(f"Skipped {skipped} — already indexed. Use Clear All to re-index.")
        else:
            gr.Warning("Nothing added. Only .pdf and .md files are supported.")
        return None, format_file_list()
    
    def clear_handler():
        try:
            doc_manager.clear_all()
            gr.Info("Knowledge base cleared.")
        except Exception as exc:
            gr.Error(f"Unable to clear documents: {exc}")
        return format_file_list()
    
    def chat_handler(msg, hist):
        for chunk in chat_interface.chat(msg, hist):
            yield chunk

    def clear_chat_handler():
        chat_interface.clear_session()

    # ---- Draft Reply tab handlers ----
    def _context_md(answer, passages, notes):
        parts = [answer or "_No grounded answer was found in the documents._"]
        if passages:
            parts.append("\n\n**Passages the answer rests on**")
            for p in passages:
                snippet = p["text"][:320] + ("…" if len(p["text"]) > 320 else "")
                parts.append(f"\n> {snippet}\n> — *{p['source']}*")
        if notes:
            parts.append("\n\n**Reviewer flagged (for your judgement)**")
            parts += [f"\n- {n}" for n in notes]
        return "\n".join(parts)

    def draft_reply_handler(incoming):
        incoming = (incoming or "").strip()
        if not incoming:
            return gr.update(), "", "", "Enter a message to respond to first."
        r = rag_system.start_reply(incoming)
        if r["needs_clarification"]:
            return (
                f"**Needs more detail:** {r['answer']}",
                "", r["thread_id"],
                "Add the missing detail above and click *Research & draft* again.",
            )
        status = "Draft ready for review. Edit as needed, then approve or discard."
        if r["critique_notes"]:
            status += "  _(reviewer left notes — see the context panel)_"
        return _context_md(r["answer"], r["passages"], r["critique_notes"]), r["draft"], r["thread_id"], status

    def revise_reply_handler(thread_id, instructions, current_draft):
        if not thread_id:
            return current_draft, "Draft something first."
        if not (instructions or "").strip():
            return current_draft, "Type what to change, then click Redraft."
        r = rag_system.revise_reply(thread_id, instructions)
        return r["draft"], "Redrafted. Edit as needed, then approve or discard."

    def approve_reply_handler(thread_id, final_text):
        if not thread_id:
            return "Nothing to approve - draft a reply first."
        if not (final_text or "").strip():
            return "The reply is empty."
        r = rag_system.approve_reply(thread_id, final_text)
        return f"Approved. Delivered to {r['delivered_to']}. Recorded at `{r['path']}`."

    def discard_reply_handler(thread_id):
        if thread_id:
            rag_system.discard_reply(thread_id)
        return "", "", "", "Discarded. Nothing was saved or delivered."

    # ---- Chat tab handlers ----
    def chat_submit(message, history):
        message = (message or "").strip()
        history = history or []
        if not message:
            yield history, ""
            return
        history = history + [{"role": "user", "content": message}]
        yield history, ""
        for msgs in chat_interface.chat(message, history):
            if isinstance(msgs, str):
                msgs = [{"role": "assistant", "content": msgs}]
            yield history + msgs, ""

    def chat_reset():
        clear_chat_handler()
        return [], ""

    # ---- Activity tab ----
    def activity_handler():
        s = rag_system.activity_summary()
        if not s["total"]:
            return "_No decisions recorded yet. Approve or discard a draft first._", ""
        edit_pct = f"{s['avg_edit_ratio'] * 100:.0f}%" if s["avg_edit_ratio"] is not None else "—"
        rounds = s["avg_critique_rounds"] if s["avg_critique_rounds"] is not None else "—"
        md = (
            f"**{s['total']}** decisions &nbsp;·&nbsp; **{s['approved']}** approved "
            f"({s['approved_verbatim']} verbatim) &nbsp;·&nbsp; **{s['rejected']}** rejected  \n"
            f"Average edit after drafting: **{edit_pct}** &nbsp;·&nbsp; avg reviewer rounds: **{rounds}**  \n"
            f"*A falling edit rate means the drafter is converging on what reviewers accept.*"
        )
        header = "| Time | Decision | Edit % | Revisions | Reviewer rounds | Question |\n|---|---|---|---|---|---|\n"
        body = ""
        for r in s["recent"]:
            er = r.get("edit_ratio")
            edit = f"{er * 100:.0f}%" if isinstance(er, (int, float)) else "—"
            q = (r.get("query", "") or "").replace("|", "/")[:70]
            body += (
                f"| {r.get('ts', '')[:19].replace('T', ' ')} | {r.get('decision', '')} | {edit} "
                f"| {r.get('revisions', 0)} | {r.get('critique_rounds', 0)} | {q} |\n"
            )
        return md, header + body

    header_html = """
    <div class="app-header">
      <div class="title">Document Assistant<span class="thin"> — grounded answers &amp; supervised replies</span></div>
      <div class="meta"><span class="dot"></span>Every reply requires human approval</div>
    </div>
    """
    footer_html = (
        '<div class="app-footer"><span>Retrieval-augmented · answers cite their sources</span>'
        '<span>Approved replies are recorded in outbox/ with an audit trail</span></div>'
    )

    with gr.Blocks(title="Document Assistant") as demo:
        gr.HTML(header_html)

        with gr.Tab("Documents", elem_id="doc-management-tab"):
            gr.Markdown("Upload PDF or Markdown files to the knowledge base. Existing files are skipped; use Clear All to re-index.")
            
            files_input = gr.File(
                label="Knowledge base files",
                file_count="multiple",
                type="filepath",
                height=200,
                show_label=False
            )
            
            add_btn = gr.Button("Add to knowledge base", variant="primary", size="md")
            
            gr.Markdown("## Indexed documents")
            file_list = gr.Textbox(
                value=format_file_list(),
                interactive=False,
                lines = 7,
                max_lines=10,
                elem_id="file-list-box",
                show_label=False
            )
            
            with gr.Row():
                refresh_btn = gr.Button("Refresh", size="md")
                clear_btn = gr.Button("Clear All", variant="stop", size="md")
            
            add_btn.click(upload_handler, [files_input], [files_input, file_list], show_progress="corner")
            refresh_btn.click(format_file_list, None, file_list)
            clear_btn.click(clear_handler, None, file_list)
        
        with gr.Tab("Chat"):
            gr.Markdown("Answers are drawn only from the indexed documents and cite their sources.")
            chatbot = gr.Chatbot(
                height=460,
                placeholder="<strong>Ask a question about the indexed documents.</strong>",
                show_label=False,
                avatar_images=(None, os.path.join(ASSETS_DIR, "chatbot_avatar.png")),
                layout="bubble",
            )
            with gr.Row(equal_height=True):
                chat_in = gr.Textbox(
                    placeholder="Ask a question about the indexed documents…",
                    show_label=False, scale=8, container=False, lines=1, max_lines=4,
                )
                chat_send = gr.Button("Send", variant="primary", scale=1, min_width=90)
            chat_clear = gr.Button("Clear conversation", variant="secondary", size="sm")

            chat_send.click(chat_submit, [chat_in, chatbot], [chatbot, chat_in])
            chat_in.submit(chat_submit, [chat_in, chatbot], [chatbot, chat_in])
            chat_clear.click(chat_reset, None, [chatbot, chat_in])

        if config.HITL_REPLY_ENABLED:
            with gr.Tab("Draft Reply"):
                gr.Markdown(
                    "Paste an incoming message. The system researches a grounded answer, drafts a reply, "
                    "and holds it for your review. The reply is delivered only after you approve it."
                )
                reply_thread = gr.State("")

                incoming_box = gr.Textbox(
                    label="Incoming message",
                    lines=4,
                    placeholder="e.g. Hi, can a monthly customer still get a refund 10 days after being charged?",
                )
                draft_start_btn = gr.Button("Research & draft", variant="primary")

                with gr.Accordion("Researched answer, passages & reviewer notes", open=False):
                    research_box = gr.Markdown()

                draft_box = gr.Textbox(
                    label="Proposed reply (editable)",
                    lines=16,
                    interactive=True,
                )
                with gr.Row():
                    revise_box = gr.Textbox(
                        label="Request changes (optional)",
                        placeholder="e.g. make it shorter and drop the greeting",
                        lines=2,
                        scale=3,
                    )
                    revise_btn = gr.Button("Redraft", scale=1)
                with gr.Row():
                    approve_btn = gr.Button("Approve & deliver", variant="primary")
                    discard_btn = gr.Button("Discard", variant="stop")

                reply_status = gr.Markdown()

                draft_start_btn.click(
                    draft_reply_handler,
                    [incoming_box],
                    [research_box, draft_box, reply_thread, reply_status],
                )
                revise_btn.click(
                    revise_reply_handler,
                    [reply_thread, revise_box, draft_box],
                    [draft_box, reply_status],
                )
                approve_btn.click(
                    approve_reply_handler,
                    [reply_thread, draft_box],
                    [reply_status],
                )
                discard_btn.click(
                    discard_reply_handler,
                    [reply_thread],
                    [research_box, draft_box, reply_thread, reply_status],
                )

            with gr.Tab("Activity"):
                gr.Markdown(
                    "Each approval and rejection is recorded, with the edit distance between the "
                    "drafted reply and the version you approved. A falling edit rate indicates "
                    "the drafter is converging on what reviewers accept."
                )
                activity_md = gr.Markdown()
                activity_table = gr.Markdown()
                activity_refresh = gr.Button("Refresh", variant="secondary", size="sm")
                demo.load(activity_handler, None, [activity_md, activity_table])
                activity_refresh.click(activity_handler, None, [activity_md, activity_table])
                approve_btn.click(activity_handler, None, [activity_md, activity_table])
                discard_btn.click(activity_handler, None, [activity_md, activity_table])

        gr.HTML(footer_html)

    return demo
