custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600&display=swap');

/* Warm, quiet, mostly borderless. Separation comes from background shifts and
   whitespace, not outlines. One muted accent, sentence-case labels. */
:root, .gradio-container, gradio-app {
    --bg:        #18171a;
    --raised:    #201f22;
    --sunken:    #131215;
    --line:      #2c2b2f;
    --text:      #e8e6e2;
    --text-dim:  #9c9891;
    --accent:    #cda06a;   /* muted warm gold, used sparingly */
    --accent-dim:#8a6f4a;

    --body-background-fill: var(--bg);
    --background-fill-primary: var(--bg);
    --background-fill-secondary: var(--raised);
    --block-background-fill: var(--bg);
    --panel-background-fill: var(--bg);
    --block-border-color: transparent;
    --border-color-primary: var(--line);
    --body-text-color: var(--text);
    --body-text-color-subdued: var(--text-dim);
    --block-label-text-color: var(--text-dim);
    --input-background-fill: var(--sunken);
    --input-border-color: var(--line);
    --button-primary-background-fill: var(--accent);
    --button-primary-text-color: #1c1710;
    --button-secondary-background-fill: var(--raised);
    --button-secondary-text-color: var(--text);
    --color-accent: var(--accent);
    --color-accent-soft: rgba(205,160,106,0.14);
    --link-text-color: var(--accent);
    --radius-sm: 8px; --radius-md: 10px; --radius-lg: 12px; --radius-xl: 14px;
}

.gradio-container {
    max-width: 860px !important;
    margin: 0 auto !important;
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}
.gradio-container p, .gradio-container li, .gradio-container span { color: var(--text) !important; }
footer { display: none !important; }
.progress-text { display: none !important; }
* { box-shadow: none !important; }

.gradio-container h1, .gradio-container h2, .gradio-container h3, .gradio-container h4 {
    color: var(--text) !important; font-weight: 600 !important; letter-spacing: -0.01em !important;
}
.gradio-container h2 { font-size: 21px !important; margin: 6px 0 2px 0 !important; }
.app-intro { color: var(--text-dim) !important; font-size: 14px !important; margin: 0 0 18px 0 !important; }

/* Tabs - sentence case, no box */
.tab-nav { border: none !important; border-bottom: 1px solid var(--line) !important; margin-bottom: 20px !important; gap: 4px !important; }
.tab-nav button {
    color: var(--text-dim) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    font-family: inherit !important;
    font-size: 14px !important; font-weight: 500 !important; letter-spacing: 0 !important;
    text-transform: none !important;
    padding: 8px 12px !important;
}
.tab-nav button:hover { color: var(--text) !important; }
.tab-nav button.selected { color: var(--text) !important; border-bottom: 2px solid var(--accent) !important; }

/* Blocks - no borders, no card backgrounds */
.block, .form, .gr-box, .panel, .gr-group {
    background: transparent !important;
    border: none !important;
}
.gradio-container label, .block-label, .block-title {
    font-family: inherit !important;
    font-size: 13px !important; font-weight: 500 !important; letter-spacing: 0 !important;
    text-transform: none !important; color: var(--text-dim) !important;
}

/* Inputs - soft, sunken, hairline border only */
input, textarea {
    background: var(--sunken) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: inherit !important;
    font-size: 15px !important;
    padding: 11px 13px !important;
}
input::placeholder, textarea::placeholder { color: var(--text-dim) !important; }
input:focus, textarea:focus { border-color: var(--accent-dim) !important; outline: none !important; }

.file-preview, [data-testid="file-upload"], .upload-container, .file-upload,
.gradio-container .file, div[data-testid="block-info"] + div .wrap {
    background: var(--raised) !important;
    border: 1.5px dashed #4a4750 !important;
    border-radius: 12px !important;
    min-height: 160px !important;
    cursor: pointer !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}
.file-preview:hover, [data-testid="file-upload"]:hover, .upload-container:hover {
    border-color: var(--accent-dim) !important;
    background: #262529 !important;
}
[data-testid="file-upload"] *, .file-preview *, .upload-container * { color: var(--text) !important; }
[data-testid="file-upload"] svg, .upload-container svg { color: var(--text-dim) !important; }
#file-list-box { background: transparent !important; border: none !important; }
#file-list-box textarea { background: var(--sunken) !important; font-size: 14px !important; }

/* Buttons - pill-ish, soft */
button.primary, button.secondary, button.stop {
    border-radius: 10px !important;
    font-weight: 600 !important; font-size: 14px !important;
    border: 1px solid transparent !important;
    padding: 9px 16px !important;
}
button.primary { background: var(--accent) !important; color: #1c1710 !important; }
button.primary:hover { background: #d8ad78 !important; }
button.secondary { background: var(--raised) !important; color: var(--text) !important; border-color: var(--line) !important; }
button.secondary:hover { background: #2a292d !important; }
button.stop { background: transparent !important; color: #d98a80 !important; border-color: #4a3835 !important; }
button.stop:hover { background: rgba(217,138,128,0.10) !important; }

/* Accordion - flat */
.gradio-container details, .accordion {
    background: var(--raised) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
}
.gradio-container details summary { color: var(--text-dim) !important; font-size: 14px !important; }

/* Chat - one soft container, no per-message boxes for the assistant */
.chatbot, .chatbot .message-wrap {
    background: var(--raised) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
}
.chatbot .message-wrap > div { padding: 18px !important; gap: 18px !important; }
.chatbot .message-row { margin-bottom: 4px !important; }
.chatbot .message, .chatbot .message p, .chatbot .message li {
    font-size: 15px !important; line-height: 1.72 !important;
}
.chatbot .message p { margin: 0 0 10px 0 !important; }
.chatbot .message p:last-child { margin-bottom: 0 !important; }

.chatbot .message.user, .chatbot .bubble.user {
    background: var(--sunken) !important;
    color: var(--text) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
}
.chatbot .message.bot, .chatbot .bubble.bot {
    background: transparent !important;
    color: var(--text) !important;
    border: none !important;
    border-left: 2px solid var(--accent-dim) !important;
    border-radius: 0 !important;
    padding: 2px 0 2px 16px !important;
    max-width: 100% !important;
}
.chatbot .message.bot strong { color: #fff !important; }
.chatbot .message.bot h1, .chatbot .message.bot h2,
.chatbot .message.bot h3, .chatbot .message.bot h4 {
    font-size: 15px !important; font-weight: 600 !important; margin: 2px 0 8px 0 !important;
}
.chatbot .message.bot hr { border: none !important; border-top: 1px solid var(--line) !important; margin: 6px 0 12px 0 !important; }
.chatbot .message.bot blockquote {
    margin: 6px 0 0 0 !important;
    padding: 4px 0 4px 14px !important;
    background: transparent !important;
    border-left: 2px solid var(--accent) !important;
    border-radius: 0 !important;
    color: var(--text-dim) !important;
}
.chatbot .message.bot blockquote p { margin: 0 !important; }
.chatbot .message.bot code {
    background: var(--sunken) !important; color: var(--accent) !important;
    padding: 1px 5px !important; border-radius: 4px !important; font-size: 13px !important;
}
.chatbot .message.bot pre {
    background: var(--sunken) !important; border: 1px solid var(--line) !important;
    border-radius: 10px !important; padding: 12px !important; overflow-x: auto !important;
}
.chatbot .message.bot pre code { color: var(--text) !important; background: transparent !important; }
.chatbot .message.bot table { border-collapse: collapse !important; }
.chatbot .message.bot td, .chatbot .message.bot th { border: 1px solid var(--line) !important; padding: 7px 11px !important; }
.chatbot .message.bot a { color: var(--accent) !important; }
.chatbot .avatar-container { display: none !important; }

.chatbot .message-wrap details {
    background: var(--sunken) !important; border: 1px solid var(--line) !important;
    font-size: 13px !important; color: var(--text-dim) !important;
}
.progress-bar { background: var(--accent) !important; }
"""
