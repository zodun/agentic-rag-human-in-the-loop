
# The look comes from a built-in Gradio theme (see app.py). This file only holds
# a few small, safe adjustments on top of it.
custom_css = """
.gradio-container { max-width: 780px !important; margin: 0 auto !important; }
footer { display: none !important; }
.app-title { font-size: 20px !important; font-weight: 650 !important; margin: 6px 0 2px 0 !important; }
.app-note  { font-size: 14px !important; opacity: 0.72; margin: 0 0 16px 0 !important; }
.chatbot .message, .chatbot .message p { font-size: 15px !important; line-height: 1.7 !important; }
.gradio-container table { font-size: 13px !important; }
"""
