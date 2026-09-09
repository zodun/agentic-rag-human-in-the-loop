custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&display=swap');

/* Considered light theme: one blue brand colour + semantic accents
   (emerald = approved, amber = needs review, rose = discard), consistent
   elevated cards, one spacing rhythm. */
:root, .gradio-container, gradio-app {
    --page:   #f3f4f7;
    --card:   #ffffff;
    --ink:    #111827;
    --ink-2:  #4b5563;
    --ink-3:  #9aa1ac;
    --line:   #e6e8ec;
    --line-2: #d7dae0;

    --brand:      #2563eb;
    --brand-hover:#1d4ed8;
    --brand-tint: #eef4ff;
    --brand-line: #cbdcff;

    --ok:      #047857;
    --ok-tint: #e9f6f0;
    --warn:      #b45309;
    --warn-tint: #fdf3e6;
    --bad:      #b91c1c;
    --bad-line: #e7c3c3;

    --shadow-sm: 0 1px 2px rgba(17,24,39,.06);
    --shadow:    0 1px 3px rgba(17,24,39,.08), 0 1px 2px rgba(17,24,39,.05);

    --body-background-fill: var(--page);
    --background-fill-primary: var(--page);
    --background-fill-secondary: var(--card);
    --block-background-fill: transparent;
    --panel-background-fill: var(--card);
    --border-color-primary: var(--line);
    --body-text-color: var(--ink);
    --body-text-color-subdued: var(--ink-2);
    --block-label-text-color: var(--ink-2);
    --input-background-fill: var(--card);
    --input-border-color: var(--line-2);
    --button-primary-background-fill: var(--brand);
    --button-primary-text-color: #ffffff;
    --button-secondary-background-fill: var(--card);
    --button-secondary-text-color: var(--ink);
    --color-accent: var(--brand);
    --link-text-color: var(--brand);
    --radius-sm: 6px; --radius-md: 8px; --radius-lg: 10px; --radius-xl: 12px;
}

.gradio-container {
    max-width: 980px !important;
    margin: 0 auto !important;
    background: var(--page) !important;
    color: var(--ink) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 0 24px 48px !important;
}
.gradio-container p, .gradio-container li, .gradio-container span { color: var(--ink) !important; }
footer { display: none !important; }
.progress-text { display: none !important; }

.gradio-container h1, .gradio-container h2, .gradio-container h3, .gradio-container h4 {
    color: var(--ink) !important; font-weight: 600 !important; letter-spacing: -0.01em !important;
}
.gradio-container h2 { font-size: 15px !important; margin: 4px 0 10px 0 !important; color: var(--ink-2) !important; }

/* ---- Masthead ---- */
.app-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 4px 16px 4px;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--line-2);
}
.app-header .title { font-size: 17px; font-weight: 700; color: var(--ink); letter-spacing: -0.015em; }
.app-header .title .thin { font-weight: 400; color: var(--ink-3); }
.app-header .meta {
    font-size: 12px; font-weight: 500; color: var(--ok);
    background: var(--ok-tint); padding: 5px 11px; border-radius: 999px;
    display: inline-flex; align-items: center; gap: 7px;
}
.app-header .meta .dot { width: 6px; height: 6px; border-radius: 999px; background: var(--ok); display: inline-block; }
.app-footer {
    margin-top: 26px; padding: 14px 4px 0; border-top: 1px solid var(--line);
    font-size: 11.5px; color: var(--ink-3); display: flex; justify-content: space-between; gap: 16px;
}

/* ---- Tabs ---- */
.tab-nav { border: none !important; border-bottom: 1px solid var(--line-2) !important; margin-bottom: 0 !important; gap: 2px !important; }
.tab-nav button {
    color: var(--ink-2) !important; background: transparent !important;
    border: none !important; border-bottom: 2px solid transparent !important; border-radius: 0 !important;
    font-family: inherit !important; font-size: 13.5px !important; font-weight: 500 !important;
    text-transform: none !important; letter-spacing: 0 !important; padding: 10px 16px !important;
}
.tab-nav button:hover { color: var(--ink) !important; }
.tab-nav button.selected { color: var(--brand) !important; border-bottom: 2px solid var(--brand) !important; }

/* ---- Tab content = one consistent card ---- */
.tabitem, [role="tabpanel"], .tab-container > div:not(.tab-nav) {
    background: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    box-shadow: var(--shadow) !important;
    padding: 22px !important;
    margin-bottom: 4px !important;
}
.tabitem > .gap, .tabitem > div, [role="tabpanel"] > div { gap: 16px !important; }

/* ---- Blocks: transparent, no nested boxes ---- */
.block, .form, .gr-box, .panel, .gr-group { background: transparent !important; border: none !important; box-shadow: none !important; }
.gradio-container label, .block-label, .block-title {
    font-family: inherit !important; font-size: 12.5px !important; font-weight: 500 !important;
    letter-spacing: 0 !important; text-transform: none !important; color: var(--ink-2) !important;
    margin-bottom: 5px !important;
}

/* ---- Inputs ---- */
input, textarea {
    background: var(--card) !important;
    border: 1px solid var(--line-2) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
    font-family: inherit !important; font-size: 14px !important;
    padding: 10px 12px !important;
}
input::placeholder, textarea::placeholder { color: var(--ink-3) !important; }
input:focus, textarea:focus {
    border-color: var(--brand) !important; outline: none !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important;
}

.file-preview, [data-testid="file-upload"], .upload-container {
    background: var(--brand-tint) !important;
    border: 1.5px dashed var(--brand-line) !important;
    border-radius: 10px !important;
    min-height: 150px !important;
    cursor: pointer !important;
}
.file-preview:hover, [data-testid="file-upload"]:hover, .upload-container:hover {
    border-color: var(--brand) !important; background: #e4edff !important;
}
[data-testid="file-upload"] *, .file-preview *, .upload-container * { color: var(--ink-2) !important; }
#file-list-box { background: transparent !important; border: none !important; }
#file-list-box textarea { background: var(--page) !important; font-size: 13px !important; border-color: var(--line) !important; }

/* ---- Buttons ---- */
button.primary, button.secondary, button.stop {
    border-radius: 8px !important; font-weight: 600 !important; font-size: 13.5px !important;
    border: 1px solid transparent !important; padding: 9px 18px !important;
    box-shadow: var(--shadow-sm) !important;
}
button.primary { background: var(--brand) !important; color: #fff !important; }
button.primary:hover { background: var(--brand-hover) !important; }
button.secondary { background: var(--card) !important; color: var(--ink) !important; border-color: var(--line-2) !important; }
button.secondary:hover { background: #f7f8fa !important; }
button.stop { background: var(--card) !important; color: var(--bad) !important; border-color: var(--bad-line) !important; box-shadow: none !important; }
button.stop:hover { background: #fdf2f2 !important; }

/* ---- Accordion ---- */
.gradio-container details, .accordion {
    background: var(--page) !important; border: 1px solid var(--line) !important; border-radius: 8px !important;
}
.gradio-container details summary { color: var(--ink-2) !important; font-size: 13px !important; padding: 10px 12px !important; }

/* ---- Chat ---- */
.chatbot, .chatbot .message-wrap {
    background: var(--card) !important; border: 1px solid var(--line) !important; border-radius: 10px !important;
}
.chatbot .message-wrap > div { padding: 18px !important; gap: 16px !important; }
.chatbot .message, .chatbot .message p, .chatbot .message li { font-size: 14px !important; line-height: 1.72 !important; }
.chatbot .message p { margin: 0 0 10px 0 !important; }
.chatbot .message p:last-child { margin-bottom: 0 !important; }
.chatbot .message.user, .chatbot .bubble.user {
    background: var(--brand-tint) !important; color: var(--ink) !important; border: 1px solid var(--brand-line) !important;
    border-radius: 8px !important; padding: 10px 13px !important;
}
.chatbot .message.bot, .chatbot .bubble.bot {
    background: transparent !important; color: var(--ink) !important;
    border: none !important; border-left: 2px solid var(--brand) !important;
    border-radius: 0 !important; padding: 2px 0 2px 14px !important; max-width: 100% !important;
}
.chatbot .message.bot strong { color: var(--ink) !important; font-weight: 600 !important; }
.chatbot .message.bot h1, .chatbot .message.bot h2,
.chatbot .message.bot h3, .chatbot .message.bot h4 { font-size: 14px !important; font-weight: 600 !important; margin: 2px 0 8px 0 !important; }
.chatbot .message.bot hr { border: none !important; border-top: 1px solid var(--line) !important; margin: 6px 0 12px 0 !important; }
.chatbot .message.bot blockquote {
    margin: 6px 0 0 0 !important; padding: 8px 12px !important;
    background: var(--brand-tint) !important; border-left: 3px solid var(--brand) !important;
    border-radius: 0 6px 6px 0 !important; color: var(--ink-2) !important;
}
.chatbot .message.bot blockquote p { margin: 0 !important; }
.chatbot .message.bot code {
    background: var(--page) !important; color: var(--warn) !important;
    padding: 1px 5px !important; border-radius: 4px !important; font-size: 12.5px !important;
}
.chatbot .message.bot pre { background: var(--page) !important; border: 1px solid var(--line) !important; border-radius: 8px !important; padding: 12px !important; overflow-x: auto !important; }
.chatbot .message.bot pre code { color: var(--ink) !important; background: transparent !important; }
.chatbot .message.bot table { border-collapse: collapse !important; }
.chatbot .message.bot td, .chatbot .message.bot th { border: 1px solid var(--line) !important; padding: 7px 11px !important; }
.chatbot .message.bot th { background: var(--page) !important; font-weight: 600 !important; }
.chatbot .message.bot a { color: var(--brand) !important; }
.chatbot .avatar-container { display: none !important; }
.chatbot .message-wrap details { background: var(--page) !important; border: 1px solid var(--line) !important; font-size: 12.5px !important; color: var(--ink-2) !important; }

/* ---- Dataframe (Activity) ---- */
.gradio-container table { border-collapse: collapse !important; font-size: 13px !important; border-radius: 8px !important; overflow: hidden !important; }
.gradio-container thead th {
    background: var(--brand-tint) !important; color: var(--ink-2) !important; font-weight: 600 !important;
    text-transform: none !important; border-bottom: 1px solid var(--brand-line) !important; padding: 8px 10px !important;
}
.gradio-container tbody td { border-bottom: 1px solid var(--line) !important; color: var(--ink) !important; padding: 7px 10px !important; }

.progress-bar { background: var(--brand) !important; }
"""
