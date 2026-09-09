custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600&display=swap');

/* Light, restrained. Near-default Gradio with one blue accent and readable type. */
:root, .gradio-container, gradio-app {
    --brand:      #2563eb;
    --brand-hover:#1d4ed8;
    --ink:  #1f2430;
    --ink-2:#5b6472;
    --line: #e5e7eb;

    --body-text-color: var(--ink);
    --body-text-color-subdued: var(--ink-2);
    --color-accent: var(--brand);
    --link-text-color: var(--brand);
    --button-primary-background-fill: var(--brand);
    --button-primary-background-fill-hover: var(--brand-hover);
    --button-primary-text-color: #ffffff;
    --border-color-primary: var(--line);
    --radius-sm: 6px; --radius-md: 8px; --radius-lg: 10px;
}

.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    color: var(--ink) !important;
    padding-top: 8px !important;
}
.gradio-container p, .gradio-container li, .gradio-container span { color: var(--ink) !important; }

/* every tab's content fills the same width */
[role="tabpanel"], [role="tabpanel"] > div, .tabitem,
.gradio-container .form, .gradio-container .block, .gradio-container .prose {
    max-width: 100% !important;
    width: 100% !important;
}
[role="tabpanel"] { display: flex !important; flex-direction: column !important; gap: 14px !important; }

footer { display: none !important; }
.progress-text { font-size: 12px !important; }

.gradio-container h1, .gradio-container h2, .gradio-container h3, .gradio-container h4 {
    color: var(--ink) !important; font-weight: 600 !important;
}
.gradio-container h2 { font-size: 15px !important; margin: 16px 0 8px 0 !important; }
.app-title { font-size: 18px !important; font-weight: 600 !important; margin: 4px 0 2px 0 !important; }
.app-note  { color: var(--ink-2) !important; font-size: 13px !important; margin: 0 0 14px 0 !important; }

/* Tabs */
.tab-nav { border-bottom: 1px solid var(--line) !important; margin-bottom: 18px !important; }
.tab-nav button {
    color: var(--ink-2) !important; background: transparent !important;
    border: none !important; border-bottom: 2px solid transparent !important; border-radius: 0 !important;
    font-size: 13.5px !important; font-weight: 500 !important; text-transform: none !important;
    padding: 9px 14px !important;
}
.tab-nav button:hover { color: var(--ink) !important; }
.tab-nav button.selected { color: var(--brand) !important; border-bottom: 2px solid var(--brand) !important; }

/* Labels */
.gradio-container label, .block-label, .block-title {
    font-size: 12.5px !important; font-weight: 500 !important; color: var(--ink-2) !important;
    text-transform: none !important; letter-spacing: 0 !important;
}

/* Inputs */
input, textarea {
    border-radius: 8px !important; font-size: 14px !important;
    color: var(--ink) !important;
}
input:focus, textarea:focus { border-color: var(--brand) !important; box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important; }

/* Buttons */
button.primary { font-weight: 600 !important; }
button.stop { color: #b91c1c !important; }

/* Chat */
.chatbot .message, .chatbot .message p, .chatbot .message li { font-size: 14px !important; line-height: 1.7 !important; }
.chatbot .message p { margin: 0 0 10px 0 !important; }
.chatbot .message p:last-child { margin-bottom: 0 !important; }
.chatbot .message.bot blockquote {
    border-left: 3px solid var(--brand) !important; padding: 6px 12px !important;
    background: #f3f6fd !important; border-radius: 0 6px 6px 0 !important; color: var(--ink-2) !important; margin: 6px 0 0 0 !important;
}
.chatbot .message.bot blockquote p { margin: 0 !important; }
.chatbot .message.bot hr { border: none !important; border-top: 1px solid var(--line) !important; margin: 6px 0 12px 0 !important; }
.chatbot .message.bot a { color: var(--brand) !important; }
.chatbot .avatar-container { display: none !important; }

/* Markdown tables (History) */
.gradio-container table { border-collapse: collapse !important; font-size: 13px !important; }
.gradio-container thead th { background: #f3f6fd !important; color: var(--ink-2) !important; font-weight: 600 !important; border-bottom: 1px solid var(--line) !important; padding: 7px 10px !important; }
.gradio-container tbody td { border-bottom: 1px solid var(--line) !important; padding: 7px 10px !important; }
"""
