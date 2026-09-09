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
        parts = [answer or "_The files do not seem to cover this._"]
        if passages:
            parts.append("\n\n**From your files**")
            for p in passages:
                snippet = p["text"][:320] + ("…" if len(p["text"]) > 320 else "")
                parts.append(f"\n> {snippet}\n> — *{p['source']}*")
        if notes:
            parts.append("\n\n**Worth a second look**")
            parts += [f"\n- {n}" for n in notes]
        return "\n".join(parts)

    def draft_reply_handler(incoming, thread_id):
        incoming = (incoming or "").strip()
        if not incoming:
            yield gr.update(), gr.update(), thread_id, "Paste the message you want to reply to first."
            return
        yield gr.update(), "", thread_id, "⏳ Researching your files and drafting a reply… (20–40s)"
        r = rag_system.start_reply(incoming)
        if r["needs_clarification"]:
            yield (
                f"**Needs more detail:** {r['answer']}",
                "", r["thread_id"],
                "Add a bit more detail above, then try again.",
            )
            return
        status = "Here is a draft. Edit it if you want, then approve it or throw it away."
        if r["critique_notes"]:
            status += "  _(there is a note worth checking below)_"
        yield _context_md(r["answer"], r["passages"], r["critique_notes"]), r["draft"], r["thread_id"], status

    def revise_reply_handler(thread_id, instructions, current_draft):
        if not thread_id:
            yield current_draft, "Write a reply first."
            return
        if not (instructions or "").strip():
            yield current_draft, "Tell it what to change first."
            return
        yield current_draft, "⏳ Rewriting…"
        r = rag_system.revise_reply(thread_id, instructions)
        yield r["draft"], "Rewritten. Edit if you want, then approve it or throw it away."

    def approve_reply_handler(thread_id, final_text):
        if not thread_id:
            yield "There is no reply yet — write one first."
            return
        if not (final_text or "").strip():
            yield "The reply is empty."
            return
        yield "⏳ Saving…"
        r = rag_system.approve_reply(thread_id, final_text)
        yield f"Approved. Saved at `{r['path']}`."

    def discard_reply_handler(thread_id):
        if thread_id:
            rag_system.discard_reply(thread_id)
        return "", "", "", "Thrown away. Nothing was sent."

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
            return "_Nothing here yet. Approve or throw away a reply and it will show up._", ""
        edit_pct = f"{s['avg_edit_ratio'] * 100:.0f}%" if s["avg_edit_ratio"] is not None else "—"
        rounds = s["avg_critique_rounds"] if s["avg_critique_rounds"] is not None else "—"
        md = (
            f"**{s['total']}** replies handled &nbsp;·&nbsp; **{s['approved']}** approved "
            f"&nbsp;·&nbsp; **{s['rejected']}** thrown away  \n"
            f"You kept **{s['approved_verbatim']}** exactly as written. "
            f"On average you changed **{edit_pct}** of a draft before approving it.  \n"
            f"*If that number drops over time, the drafts are getting closer to what you would write.*"
        )
        header = "| When | What you did | How much you changed it | Rewrites | Checks | The message |\n|---|---|---|---|---|---|\n"
        body = ""
        for r in s["recent"]:
            er = r.get("edit_ratio")
            edit = f"{er * 100:.0f}%" if isinstance(er, (int, float)) else "—"
            q = (r.get("query", "") or "").replace("|", "/")[:70]
            did = "thrown away" if r.get("decision") == "rejected" else "approved"
            body += (
                f"| {r.get('ts', '')[:16].replace('T', ' ')} | {did} | {edit} "
                f"| {r.get('revisions', 0)} | {r.get('critique_rounds', 0)} | {q} |\n"
            )
        return md, header + body

    with gr.Blocks(title="Document Assistant") as demo:
        gr.Markdown(
            '<div class="app-title">Document Assistant</div>'
            '<p class="app-note">Ask questions about your files. Draft replies that you approve before they are sent.</p>',
            sanitize_html=False,
        )

        with gr.Tab("Documents", elem_id="doc-management-tab"):
            gr.Markdown("Add PDF or text files. The assistant only answers using what you add here.")
            
            files_input = gr.File(
                label="Files",
                file_count="multiple",
                type="filepath",
                height=200,
                show_label=False
            )
            
            add_btn = gr.Button("Add files", variant="primary", size="md")
            
            gr.Markdown("## Files you have added")
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
                clear_btn = gr.Button("Remove all", variant="stop", size="md")
            
            add_btn.click(upload_handler, [files_input], [files_input, file_list], show_progress="corner")
            refresh_btn.click(format_file_list, None, file_list)
            clear_btn.click(clear_handler, None, file_list)
        
        with gr.Tab("Chat"):
            gr.Markdown("Ask about your files. Each answer shows which file it came from.")
            chatbot = gr.Chatbot(
                height=460,
                placeholder="<strong>Ask a question about your files.</strong>",
                show_label=False,
                avatar_images=(None, os.path.join(ASSETS_DIR, "chatbot_avatar.png")),
                layout="bubble",
            )
            with gr.Row(equal_height=True):
                chat_in = gr.Textbox(
                    placeholder="Type your question…",
                    show_label=False, scale=8, container=False, lines=1, max_lines=4,
                )
                chat_send = gr.Button("Send", variant="primary", scale=1, min_width=90)
            chat_clear = gr.Button("Start over", variant="secondary", size="sm")

            chat_send.click(chat_submit, [chat_in, chatbot], [chatbot, chat_in])
            chat_in.submit(chat_submit, [chat_in, chatbot], [chatbot, chat_in])
            chat_clear.click(chat_reset, None, [chatbot, chat_in])

        if config.HITL_REPLY_ENABLED:
            with gr.Tab("Draft Reply"):
                gr.Markdown(
                    "Paste a message someone sent you. The assistant finds the answer in your files "
                    "and writes a reply. You edit and approve it — nothing is sent until you do."
                )
                reply_thread = gr.State("")

                incoming_box = gr.Textbox(
                    label="The message you got",
                    lines=3,
                    max_lines=8,
                    placeholder="e.g. Hi, can a monthly customer still get a refund 10 days after being charged?",
                )
                draft_start_btn = gr.Button("Write a reply", variant="primary")

                with gr.Accordion("What this reply is based on", open=False):
                    research_box = gr.Markdown()

                draft_box = gr.Textbox(
                    label="Draft reply — edit it however you like",
                    lines=7,
                    max_lines=16,
                    interactive=True,
                    autoscroll=False,
                )
                with gr.Row(equal_height=True):
                    revise_box = gr.Textbox(
                        label="Want it different? Say how",
                        placeholder="e.g. make it shorter and drop the greeting",
                        lines=1,
                        max_lines=3,
                        scale=4,
                        container=False,
                    )
                    revise_btn = gr.Button("Rewrite", variant="secondary", scale=1)

                with gr.Row():
                    approve_btn = gr.Button("Approve", variant="primary", scale=2)
                    discard_btn = gr.Button("Throw away", variant="stop", scale=1)

                reply_status = gr.Markdown()

                draft_start_btn.click(
                    draft_reply_handler,
                    [incoming_box, reply_thread],
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

            with gr.Tab("History"):
                gr.Markdown(
                    "A log of every reply you approved or threw away, and how much you changed "
                    "each draft before approving it."
                )
                activity_md = gr.Markdown()
                activity_table = gr.Markdown()
                activity_refresh = gr.Button("Refresh", variant="secondary", size="sm")
                demo.load(activity_handler, None, [activity_md, activity_table])
                activity_refresh.click(activity_handler, None, [activity_md, activity_table])
                approve_btn.click(activity_handler, None, [activity_md, activity_table])
                discard_btn.click(activity_handler, None, [activity_md, activity_table])

    return demo
