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
    
    with gr.Blocks(title="Agentic RAG") as demo:
        
        with gr.Tab("Documents", elem_id="doc-management-tab"):
            gr.Markdown("## Add New Documents")
            gr.Markdown("Upload PDF or Markdown files. Existing documents are skipped; use Clear All before re-indexing.")
            
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
            if config.HITL_REPLY_ENABLED:
                gr.Markdown(
                    "I answer from your uploaded documents, then draft an outbound reply and "
                    "**pause for your approval**. Reply **approve** to send it (saved to `outbox/`), "
                    "**reject** to discard, or just say what to change."
                )
            chatbot = gr.Chatbot(
                height=680,
                placeholder="<strong>Ask a question about your uploaded documents.</strong>",
                show_label=False,
                avatar_images=(None, os.path.join(ASSETS_DIR, "chatbot_avatar.png")),
                layout="bubble",
            )
            chatbot.clear(clear_chat_handler)
            
            gr.ChatInterface(fn=chat_handler, chatbot=chatbot)
    
    return demo
