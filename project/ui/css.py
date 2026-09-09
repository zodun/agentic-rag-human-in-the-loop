custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&display=swap');

/* Neutral, restrained, enterprise-tool look. Light warm-grey, slate accent,
   hairline structure, clear hierarchy. */
:root, .gradio-container, gradio-app {
    --page:   #f5f6f8;
    --panel:  #ffffff;
    --sunken: #f0f1f4;
    --line:   #e2e5ea;
    --line-strong: #d3d7de;
    --text:   #1f2733;
    --text-2: #5b6472;
    --text-3: #8b93a1;
    --accent: #3a5a8c;
    --accent-hover: #31507d;

    --body-background-fill: var(--page);
    --background-fill-primary: var(--page);
    --background-fill-secondary: var(--panel);
    --block-background-fill: var(--page);
    --panel-background-fill: var(--panel);
    --block-border-color: var(--line);
    --border-color-primary: var(--line);
    --body-text-color: var(--text);
    --body-text-color-subdued: var(--text-2);
    --block-label-text-color: var(--text-2);
    --input-background-fill: var(--panel);
    --input-border-color: var(--line-strong);
    --button-primary-background-fill: var(--accent);
    --button-primary-text-color: #ffffff;
    --button-secondary-background-fill: var(--panel);
    --button-secondary-text-color: var(--text);
    --color-accent: var(--accent);
    --link-text-color: var(--accent);
    --radius-sm: 6px; --radius-md: 8px; --radius-lg: 8px; --radius-xl: 10px;
}

.gradio-container {
    max-width: 1000px !important;
    margin: 0 auto !important;
    background: var(--page) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 0 20px 40px !important;
}
.gradio-container p, .gradio-container li, .gradio-container span { color: var(--text) !important; }
footer { display: none !important; }
.progress-text { display: none !important; }
* { box-shadow: none !important; }

.gradio-container h1, .gradio-container h2, .gradio-container h3, .gradio-container h4 {
    color: var(--text) !important; font-weight: 600 !important; letter-spacing: -0.01em !important;
}
.gradio-container h2 { font-size: 16px !important; margin: 20px 0 6px 0 !important; }

/* ---- Masthead ---- */
.app-header {
    display: flex; align-items: baseline; justify-content: space-between;
    padding: 18px 0 14px 0;
    border-bottom: 1px solid var(--line-strong);
    margin-bottom: 22px;
}
.app-header .title { font-size: 16px; font-weight: 700; color: var(--text); letter-spacing: -0.01em; }
.app-header .title .thin { font-weight: 400; color: var(--text-3); }
.app-header .meta {
    font-size: 12px; color: var(--text-2);
    display: inline-flex; align-items: center; gap: 7px;
}
.app-header .meta .dot { width: 6px; height: 6px; border-radius: 999px; background: #4a9d6b; display: inline-block; }
.app-footer {
    margin-top: 28px; padding-top: 14px; border-top: 1px solid var(--line);
    font-size: 11.5px; color: var(--text-3); display: flex; justify-content: space-between;
}

/* ---- Tabs ---- */
.tab-nav { border: none !important; border-bottom: 1px solid var(--line-strong) !important; margin-bottom: 22px !important; gap: 2px !important; }
.tab-nav button {
    color: var(--text-2) !important; background: transparent !important;
    border: none !important; border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    font-family: inherit !important; font-size: 13.5px !important; font-weight: 500 !important;
    letter-spacing: 0 !important; text-transform: none !important;
    padding: 9px 14px !important;
}
.tab-nav button:hover { color: var(--text) !important; }
.tab-nav button.selected { color: var(--accent) !important; border-bottom: 2px solid var(--accent) !important; }

/* ---- Blocks: one calm panel per working zone, not nested boxes ---- */
.block, .form, .gr-box, .panel, .gr-group { background: transparent !important; border: none !important; }
.gradio-container label, .block-label, .block-title {
    font-family: inherit !important; font-size: 12.5px !important; font-weight: 500 !important;
    letter-spacing: 0 !important; text-transform: none !important; color: var(--text-2) !important;
    margin-bottom: 4px !important;
}

/* ---- Inputs ---- */
input, textarea {
    background: var(--panel) !important;
    border: 1px solid var(--line-strong) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: inherit !important; font-size: 14px !important;
    padding: 10px 12px !important;
}
input::placeholder, textarea::placeholder { color: var(--text-3) !important; }
input:focus, textarea:focus { border-color: var(--accent) !important; outline: none !important; }

.file-preview, [data-testid="file-upload"], .upload-container {
    background: var(--panel) !important;
    border: 1.5px dashed var(--line-strong) !important;
    border-radius: 10px !important;
    min-height: 150px !important;
    cursor: pointer !important;
}
.file-preview:hover, [data-testid="file-upload"]:hover, .upload-container:hover {
    border-color: var(--accent) !important; background: #fafbfc !important;
}
[data-testid="file-upload"] *, .file-preview *, .upload-container * { color: var(--text-2) !important; }
#file-list-box { background: transparent !important; border: none !important; }
#file-list-box textarea { background: var(--sunken) !important; font-size: 13px !important; border-color: var(--line) !important; }

/* ---- Buttons ---- */
button.primary, button.secondary, button.stop {
    border-radius: 8px !important; font-weight: 600 !important; font-size: 13.5px !important;
    border: 1px solid transparent !important; padding: 9px 18px !important;
}
button.primary { background: var(--accent) !important; color: #fff !important; }
button.primary:hover { background: var(--accent-hover) !important; }
button.secondary { background: var(--panel) !important; color: var(--text) !important; border-color: var(--line-strong) !important; }
button.secondary:hover { background: #fafbfc !important; }
button.stop { background: var(--panel) !important; color: #a03530 !important; border-color: #e0c4c2 !important; }
button.stop:hover { background: #fcf5f4 !important; }

/* ---- Accordion ---- */
.gradio-container details, .accordion {
    background: var(--panel) !important; border: 1px solid var(--line) !important; border-radius: 8px !important;
}
.gradio-container details summary { color: var(--text-2) !important; font-size: 13px !important; padding: 10px 12px !important; }

/* ---- Chat: single framed panel ---- */
.chatbot, .chatbot .message-wrap {
    background: var(--panel) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
}
.chatbot .message-wrap > div { padding: 18px !important; gap: 16px !important; }
.chatbot .message, .chatbot .message p, .chatbot .message li {
    font-size: 14px !important; line-height: 1.72 !important;
}
.chatbot .message p { margin: 0 0 10px 0 !important; }
.chatbot .message p:last-child { margin-bottom: 0 !important; }
.chatbot .message.user, .chatbot .bubble.user {
    background: var(--sunken) !important; color: var(--text) !important; border: none !important;
    border-radius: 8px !important; padding: 10px 13px !important;
}
.chatbot .message.bot, .chatbot .bubble.bot {
    background: transparent !important; color: var(--text) !important;
    border: none !important; border-left: 2px solid var(--line-strong) !important;
    border-radius: 0 !important; padding: 2px 0 2px 14px !important; max-width: 100% !important;
}
.chatbot .message.bot strong { color: var(--text) !important; font-weight: 600 !important; }
.chatbot .message.bot h1, .chatbot .message.bot h2,
.chatbot .message.bot h3, .chatbot .message.bot h4 { font-size: 14px !important; font-weight: 600 !important; margin: 2px 0 8px 0 !important; }
.chatbot .message.bot hr { border: none !important; border-top: 1px solid var(--line) !important; margin: 6px 0 12px 0 !important; }
.chatbot .message.bot blockquote {
    margin: 6px 0 0 0 !important; padding: 4px 0 4px 13px !important;
    background: transparent !important; border-left: 2px solid var(--accent) !important;
    border-radius: 0 !important; color: var(--text-2) !important;
}
.chatbot .message.bot blockquote p { margin: 0 !important; }
.chatbot .message.bot code {
    background: var(--sunken) !important; color: #7a4b1e !important;
    padding: 1px 5px !important; border-radius: 4px !important; font-size: 12.5px !important;
}
.chatbot .message.bot pre {
    background: var(--sunken) !important; border: 1px solid var(--line) !important;
    border-radius: 8px !important; padding: 12px !important; overflow-x: auto !important;
}
.chatbot .message.bot pre code { color: var(--text) !important; background: transparent !important; }
.chatbot .message.bot table { border-collapse: collapse !important; }
.chatbot .message.bot td, .chatbot .message.bot th { border: 1px solid var(--line) !important; padding: 7px 11px !important; }
.chatbot .message.bot th { background: var(--sunken) !important; font-weight: 600 !important; }
.chatbot .message.bot a { color: var(--accent) !important; }
.chatbot .avatar-container { display: none !important; }
.chatbot .message-wrap details { background: var(--sunken) !important; border: 1px solid var(--line) !important; font-size: 12.5px !important; color: var(--text-2) !important; }

/* ---- Dataframe (Activity) ---- */
.gradio-container table { border-collapse: collapse !important; font-size: 13px !important; }
.gradio-container thead th {
    background: var(--sunken) !important; color: var(--text-2) !important;
    font-weight: 600 !important; text-transform: none !important; border-bottom: 1px solid var(--line-strong) !important;
}
.gradio-container tbody td { border-bottom: 1px solid var(--line) !important; color: var(--text) !important; }

.progress-bar { background: var(--accent) !important; }
"""
