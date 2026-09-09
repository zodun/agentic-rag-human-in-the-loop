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
            return "📭 No documents available in the knowledge base"
        return "\n".join([f"{f}" for f in files])
    
    def upload_handler(files, progress=gr.Progress()):
        if not files:
            return None, format_file_list()
            
        added, skipped = doc_manager.add_documents(
            files, 
            progress_callback=lambda p, desc: progress(p, desc=desc)
        )
        
        gr.Info(f"✅ Added: {added} | Skipped: {skipped}")
        return None, format_file_list()
    
    def clear_handler():
        try:
            doc_manager.clear_all()
            gr.Info("🗑️ Removed all documents")
        except Exception as exc:
            gr.Error(f"Unable to clear documents: {exc}")
        return format_file_list()
    
    def chat_handler(msg, hist):
        for chunk in chat_interface.chat(msg, hist):
            yield chunk

    def clear_chat_handler():
        chat_interface.clear_session()

    # ---- Draft Reply tab handlers ----
    def draft_reply_handler(incoming):
        incoming = (incoming or "").strip()
        if not incoming:
            return gr.update(), "", "", "Enter a message to respond to first."
        result = rag_system.start_reply(incoming)
        if result["needs_clarification"]:
            return (
                f"**Needs more detail:** {result['answer']}",
                "", result["thread_id"],
                "Add the missing detail above and click *Research & draft* again.",
            )
        answer = result["answer"] or "_No grounded answer was found in the documents._"
        return answer, result["draft"], result["thread_id"], "Draft ready. Edit it above if needed, then **Approve**."

    def revise_reply_handler(thread_id, instructions, current_draft):
        if not thread_id:
            return current_draft, "Draft something first."
        if not (instructions or "").strip():
            return current_draft, "Type what to change, then click Redraft."
        new_draft = rag_system.revise_reply(thread_id, instructions)
        return new_draft, "Redrafted. Edit above if needed, then **Approve**."

    def approve_reply_handler(thread_id, final_text):
        if not thread_id:
            return "Nothing to approve - draft a reply first."
        if not (final_text or "").strip():
            return "The reply is empty."
        path = rag_system.approve_reply(thread_id, final_text)
        return f"✅ **Approved and saved** to `{path}`"

    def discard_reply_handler(thread_id):
        if thread_id:
            rag_system.discard_reply(thread_id)
        return "", "", "", "🗑 Discarded. Nothing was saved."

    with gr.Blocks(title="Document Assistant") as demo:
        gr.Markdown(
            "## Document Assistant\n"
            '<p class="app-intro">Ask questions about your files, and draft replies you approve before they are saved.</p>',
            sanitize_html=False,
        )

        with gr.Tab("Documents", elem_id="doc-management-tab"):
            gr.Markdown("Upload PDF or Markdown files. Existing files are skipped; use *Clear All* before re-indexing.")
            
            files_input = gr.File(
                label="Drop PDF or Markdown files here",
                file_count="multiple",
                type="filepath",
                height=200,
                show_label=False
            )
            
            add_btn = gr.Button("Add Documents", variant="primary", size="md")
            
            gr.Markdown("## Current Documents in the Knowledge Base")
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
            gr.Markdown("Ask anything about your uploaded documents. Every answer is based on the documents and lists its sources.")
            chatbot = gr.Chatbot(
                height=680,
                placeholder="<strong>Ask a question about your uploaded documents.</strong>",
                show_label=False,
                avatar_images=(None, os.path.join(ASSETS_DIR, "chatbot_avatar.png")),
                layout="bubble",
            )
            chatbot.clear(clear_chat_handler)
            gr.ChatInterface(fn=chat_handler, chatbot=chatbot)

        if config.HITL_REPLY_ENABLED:
            with gr.Tab("Draft Reply"):
                gr.Markdown(
                    "Paste a message you need to answer. The system researches a grounded answer "
                    "from your documents and drafts a reply. **Edit it freely, then approve** - only "
                    "then is it written to `outbox/`."
                )
                reply_thread = gr.State("")

                incoming_box = gr.Textbox(
                    label="Incoming message / question to answer",
                    lines=4,
                    placeholder="e.g. Hi, can a monthly customer still get a refund 10 days after being charged?",
                )
                draft_start_btn = gr.Button("Research & draft reply", variant="primary")

                with gr.Accordion("Researched answer (context for the draft)", open=False):
                    research_box = gr.Markdown()

                draft_box = gr.Textbox(
                    label="Proposed reply — edit before approving",
                    lines=16,
                    interactive=True,
                )
                with gr.Row():
                    revise_box = gr.Textbox(
                        label="Ask for changes (optional)",
                        placeholder="e.g. make it shorter and drop the greeting",
                        lines=2,
                        scale=3,
                    )
                    revise_btn = gr.Button("Redraft with changes", scale=1)
                with gr.Row():
                    approve_btn = gr.Button("✅ Approve & save to outbox", variant="primary")
                    discard_btn = gr.Button("🗑 Discard", variant="stop")

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

    return demo
