custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600&display=swap');

/* Self-contained light theme: paints its own surfaces so it stays readable even
   if Gradio renders in dark mode. Narrow column, high-contrast text. */
:root {
    --brand:  #2563eb;
    --brand-hover: #1d4ed8;
    --ink:    #111827;
    --ink-2:  #4b5563;
    --line:   #e4e6eb;
    --page:   #f7f8fa;
    --card:   #ffffff;
}

html, body, gradio-app, .gradio-container {
    background: var(--page) !important;
    color: var(--ink) !important;
}
.gradio-container {
    max-width: 720px !important;
    margin: 0 auto !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 10px 16px 40px !important;
}
.gradio-container *, .gradio-container p, .gradio-container li,
.gradio-container span, .gradio-container label, .gradio-container div {
    color: var(--ink);
}
.gradio-container .block-label, .gradio-container label span,
.gradio-container .block-title { color: var(--ink-2) !important; }
footer { display: none !important; }

.gradio-container h1, .gradio-container h2, .gradio-container h3, .gradio-container h4 {
    color: var(--ink) !important; font-weight: 600 !important;
}
.gradio-container h2 { font-size: 15px !important; margin: 16px 0 8px 0 !important; }
.app-title { font-size: 18px !important; font-weight: 600 !important; margin: 4px 0 2px 0 !important; }
.app-note  { color: var(--ink-2) !important; font-size: 13px !important; margin: 0 0 14px 0 !important; }

/* Tabs */
.tab-nav { border-bottom: 1px solid var(--line) !important; margin-bottom: 18px !important; background: transparent !important; }
.tab-nav button {
    color: var(--ink-2) !important; background: transparent !important;
    border: none !important; border-bottom: 2px solid transparent !important; border-radius: 0 !important;
    font-size: 13.5px !important; font-weight: 500 !important; padding: 9px 14px !important;
}
.tab-nav button:hover { color: var(--ink) !important; }
.tab-nav button.selected { color: var(--brand) !important; border-bottom: 2px solid var(--brand) !important; }

/* Panels / blocks — flat, no dark fills */
.block, .form, .panel, .gr-box, .gr-group, [role="tabpanel"] {
    background: transparent !important; border: none !important; box-shadow: none !important;
}

/* Inputs */
input, textarea, .gr-input, [data-testid="textbox"] textarea {
    background: var(--card) !important;
    border: 1px solid #d5d8de !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
    font-size: 14px !important;
}
input::placeholder, textarea::placeholder { color: #9aa0ab !important; }
input:focus, textarea:focus { border-color: var(--brand) !important; box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important; outline: none !important; }
textarea[readonly] { background: var(--page) !important; color: var(--ink-2) !important; }

/* File box + list */
.file-preview, [data-testid="file-upload"] { background: var(--card) !important; color: var(--ink-2) !important; }
[data-testid="file-upload"] * { color: var(--ink-2) !important; }
#file-list-box textarea { background: var(--page) !important; color: var(--ink) !important; }

/* Buttons */
button.primary { background: var(--brand) !important; color: #fff !important; border: none !important; font-weight: 600 !important; }
button.primary:hover { background: var(--brand-hover) !important; }
button.secondary { background: var(--card) !important; color: var(--ink) !important; border: 1px solid #d5d8de !important; }
button.stop { background: var(--card) !important; color: #b91c1c !important; border: 1px solid #e3c4c2 !important; }

/* Accordion */
.gradio-container details, .accordion { background: var(--card) !important; border: 1px solid var(--line) !important; border-radius: 8px !important; }
.gradio-container details summary { color: var(--ink-2) !important; }

/* Chat */
.chatbot, .chatbot .message-wrap { background: var(--card) !important; border: 1px solid var(--line) !important; border-radius: 10px !important; }
.chatbot .message, .chatbot .message p, .chatbot .message li { font-size: 14px !important; line-height: 1.7 !important; color: var(--ink) !important; }
.chatbot .message p { margin: 0 0 10px 0 !important; }
.chatbot .message p:last-child { margin-bottom: 0 !important; }
.chatbot .message.user, .chatbot .bubble.user { background: #eef2fb !important; color: var(--ink) !important; border: none !important; }
.chatbot .message.bot, .chatbot .bubble.bot { background: transparent !important; color: var(--ink) !important; border: none !important; border-left: 2px solid var(--brand) !important; border-radius: 0 !important; padding-left: 12px !important; }
.chatbot .message.bot blockquote { border-left: 3px solid var(--brand) !important; padding: 6px 12px !important; background: #f3f6fd !important; border-radius: 0 6px 6px 0 !important; color: var(--ink-2) !important; margin: 6px 0 0 0 !important; }
.chatbot .message.bot blockquote p { margin: 0 !important; }
.chatbot .message.bot hr { border: none !important; border-top: 1px solid var(--line) !important; margin: 6px 0 12px 0 !important; }
.chatbot .message.bot code { background: var(--page) !important; color: #92400e !important; padding: 1px 5px !important; border-radius: 4px !important; }
.chatbot .message.bot a { color: var(--brand) !important; }
.chatbot .avatar-container { display: none !important; }

/* Tables (History) */
.gradio-container table { border-collapse: collapse !important; font-size: 13px !important; }
.gradio-container thead th { background: #f3f6fd !important; color: var(--ink-2) !important; font-weight: 600 !important; border-bottom: 1px solid var(--line) !important; padding: 7px 10px !important; }
.gradio-container tbody td { border-bottom: 1px solid var(--line) !important; color: var(--ink) !important; padding: 7px 10px !important; }

.progress-bar { background: var(--brand) !important; }
"""
