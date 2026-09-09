custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ============================================================
   Material-3 dark cockpit palette (from the LangGraph Studio mock)
   ============================================================ */
:root, .gradio-container, gradio-app {
    --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;

    --m3-bg: #0b1326;
    --m3-lowest: #060e20;
    --m3-low: #131b2e;
    --m3-container: #171f33;
    --m3-high: #222a3d;
    --m3-highest: #2d3449;
    --m3-on: #dae2fd;
    --m3-on-variant: #c7c4d7;
    --m3-outline: #908fa0;
    --m3-outline-variant: #464554;
    --m3-primary: #c0c1ff;
    --m3-primary-container: #8083ff;
    --m3-on-primary: #1000a9;
    --m3-secondary: #4edea3;
    --m3-tertiary: #ffb95f;
    --m3-error: #ffb4ab;
    --m3-error-container: #93000a;

    /* map Gradio's own theme tokens onto the palette */
    --body-background-fill: var(--m3-bg);
    --background-fill-primary: var(--m3-low);
    --background-fill-secondary: var(--m3-container);
    --block-background-fill: var(--m3-low);
    --panel-background-fill: var(--m3-low);
    --block-border-color: var(--m3-outline-variant);
    --border-color-primary: var(--m3-outline-variant);
    --border-color-accent: var(--m3-primary-container);
    --body-text-color: var(--m3-on);
    --body-text-color-subdued: var(--m3-outline);
    --block-label-text-color: var(--m3-on-variant);
    --block-title-text-color: var(--m3-on);
    --input-background-fill: var(--m3-lowest);
    --input-border-color: var(--m3-outline-variant);
    --input-border-color-focus: var(--m3-primary-container);
    --button-primary-background-fill: var(--m3-primary-container);
    --button-primary-background-fill-hover: var(--m3-primary);
    --button-primary-text-color: var(--m3-on-primary);
    --button-secondary-background-fill: var(--m3-high);
    --button-secondary-background-fill-hover: var(--m3-highest);
    --button-secondary-text-color: var(--m3-on);
    --button-cancel-background-fill: var(--m3-error-container);
    --button-cancel-text-color: #ffdad6;
    --color-accent: var(--m3-primary);
    --color-accent-soft: rgba(128,131,255,0.18);
    --link-text-color: var(--m3-primary);
    --radius-xs: 2px; --radius-sm: 4px; --radius-md: 4px; --radius-lg: 6px; --radius-xl: 8px;
    --table-border-color: var(--m3-outline-variant);
    --table-even-background-fill: var(--m3-low);
    --table-odd-background-fill: var(--m3-container);
}

.gradio-container {
    max-width: 1280px !important;
    margin: 0 auto !important;
    background: var(--m3-bg) !important;
    color: var(--m3-on) !important;
    font-family: var(--font) !important;
    font-size: 14px !important;
}
.gradio-container p, .gradio-container li, .gradio-container span, .gradio-container label {
    color: var(--m3-on) !important;
}
footer { display: none !important; }
.progress-text { display: none !important; }
* { box-shadow: none !important; }

/* ---------------- Studio chrome (static) ---------------- */
.studio-topbar {
    display: flex; align-items: center; justify-content: space-between;
    background: var(--m3-lowest);
    border: 1px solid var(--m3-outline-variant);
    border-radius: 6px;
    padding: 12px 16px; margin-bottom: 14px;
}
.studio-brand { display: flex; align-items: center; gap: 12px; }
.studio-brand .mark {
    width: 30px; height: 30px; border-radius: 6px;
    background: linear-gradient(135deg, var(--m3-primary-container), var(--m3-secondary));
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-weight: 600; color: #060e20; font-size: 14px;
}
.studio-brand .name { font-weight: 600; font-size: 16px; color: var(--m3-on); letter-spacing: -0.01em; line-height: 1.15; }
.studio-brand .sub {
    font-family: var(--font); font-size: 12.5px; color: var(--m3-on-variant);
    margin-top: 3px; max-width: 46ch;
}
.studio-pill {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 4px 9px; border-radius: 4px; background: var(--m3-high); color: var(--m3-on-variant);
}
.studio-pill .dot { width: 6px; height: 6px; border-radius: 999px; background: var(--m3-secondary); }
.studio-pill.warn { color: var(--m3-tertiary); background: rgba(255,185,95,0.14); }
.studio-pill.warn .dot { background: var(--m3-tertiary); }

.studio-steps {
    display: flex; flex-wrap: wrap; gap: 14px 18px; align-items: center;
    background: var(--m3-low); border: 1px solid var(--m3-outline-variant);
    border-radius: 6px; padding: 12px 16px; margin-bottom: 18px;
    font-family: var(--font); font-size: 13px; color: var(--m3-on-variant);
}
.studio-steps .n {
    display: inline-flex; align-items: center; justify-content: center;
    width: 18px; height: 18px; border-radius: 999px; margin-right: 7px;
    background: var(--m3-high); color: var(--m3-primary);
    font-family: var(--font-mono); font-size: 11px; font-weight: 600;
}
.studio-steps .arrow { color: var(--m3-outline); }

.studio-eyebrow {
    font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--m3-outline);
    margin: 4px 0 2px 0 !important;
}

/* ---------------- Tabs ---------------- */
.tab-nav { border-bottom: 1px solid var(--m3-outline-variant) !important; }
.tab-nav button {
    color: var(--m3-outline) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important; letter-spacing: 0.04em !important;
    text-transform: uppercase !important; font-weight: 600 !important;
    padding: 10px 16px !important;
}
.tab-nav button:hover { color: var(--m3-on) !important; }
.tab-nav button.selected {
    color: var(--m3-on) !important;
    border-bottom: 2px solid var(--m3-primary) !important;
}

/* ---------------- Blocks / cards ---------------- */
.block, .form, .gr-box, .panel {
    background: var(--m3-low) !important;
    border: 1px solid var(--m3-outline-variant) !important;
    border-radius: 6px !important;
}
.gradio-container label, .block-title, .block-label {
    font-family: var(--font-mono) !important;
    font-size: 11px !important; letter-spacing: 0.06em !important;
    text-transform: uppercase !important; color: var(--m3-on-variant) !important;
}

/* ---------------- Inputs ---------------- */
input, textarea, .file-preview, [data-testid="file-upload"], #file-list-box {
    background: var(--m3-lowest) !important;
    border: 1px solid var(--m3-outline-variant) !important;
    border-radius: 4px !important;
    color: var(--m3-on) !important;
    font-family: var(--font) !important;
    font-size: 14px !important;
}
input::placeholder, textarea::placeholder { color: var(--m3-outline) !important; }
input:focus, textarea:focus { border-color: var(--m3-primary-container) !important; outline: none !important; }
[data-testid="file-upload"], .file-preview { min-height: 180px !important; }
[data-testid="file-upload"] *, .file-preview * { color: var(--m3-on-variant) !important; }
#file-list-box, #file-list-box textarea {
    font-family: var(--font-mono) !important; font-size: 12px !important;
    background: var(--m3-lowest) !important;
}

/* ---------------- Buttons ---------------- */
button.primary, button.secondary, button.stop, .gr-button {
    border-radius: 4px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border: 1px solid transparent !important;
}
button.primary { background: var(--m3-primary-container) !important; color: var(--m3-on-primary) !important; }
button.primary:hover { background: var(--m3-primary) !important; }
button.secondary { background: var(--m3-high) !important; color: var(--m3-on) !important; border-color: var(--m3-outline-variant) !important; }
button.stop { background: var(--m3-error-container) !important; color: #ffdad6 !important; }

/* ---------------- Accordion ---------------- */
.gradio-container details, .accordion {
    background: var(--m3-container) !important;
    border: 1px solid var(--m3-outline-variant) !important;
    border-radius: 4px !important;
}
.gradio-container details summary { color: var(--m3-on-variant) !important; font-family: var(--font-mono) !important; font-size: 12px !important; }

/* ============================================================
   CHAT
   ============================================================ */
.chatbot, .chatbot .message-wrap {
    background: var(--m3-lowest) !important;
    border: 1px solid var(--m3-outline-variant) !important;
    border-radius: 6px !important;
}
.chatbot .message-wrap > div { padding: 16px !important; gap: 14px !important; }
.chatbot .message-row { margin-bottom: 6px !important; }

.chatbot .message, .chatbot .message p, .chatbot .message li,
.chatbot .message td, .chatbot .message th {
    font-size: 14px !important; line-height: 1.7 !important;
}
.chatbot .message p { margin: 0 0 10px 0 !important; }
.chatbot .message p:last-child { margin-bottom: 0 !important; }
.chatbot .message ul, .chatbot .message ol { margin: 6px 0 10px 0 !important; padding-left: 20px !important; }

.chatbot .message.user, .chatbot .bubble.user {
    background: var(--m3-primary-container) !important;
    color: #0d0096 !important;
    border: none !important;
    border-radius: 4px 4px 1px 4px !important;
    padding: 11px 14px !important;
}
.chatbot .message.bot, .chatbot .bubble.bot {
    background: var(--m3-container) !important;
    color: var(--m3-on) !important;
    border: 1px solid var(--m3-outline-variant) !important;
    border-radius: 4px 4px 4px 1px !important;
    max-width: 100% !important;
    padding: 14px 16px !important;
}
.chatbot .message.bot strong { color: #ffffff !important; }
.chatbot .message.bot h1, .chatbot .message.bot h2,
.chatbot .message.bot h3, .chatbot .message.bot h4 {
    color: #ffffff !important; font-size: 14px !important; font-weight: 600 !important;
    margin: 2px 0 10px 0 !important;
}
.chatbot .message.bot hr { border: none !important; border-top: 1px solid var(--m3-outline-variant) !important; margin: 2px 0 12px 0 !important; }

.chatbot .message.bot blockquote {
    margin: 2px 0 0 0 !important;
    padding: 12px 14px !important;
    background: rgba(128,131,255,0.14) !important;
    border-left: 3px solid var(--m3-primary-container) !important;
    border-radius: 4px !important;
    color: var(--m3-on) !important;
}
.chatbot .message.bot blockquote p { margin: 0 !important; }

.chatbot .message.bot code {
    font-family: var(--font-mono) !important;
    background: var(--m3-lowest) !important;
    color: var(--m3-tertiary) !important;
    padding: 2px 5px !important; border-radius: 3px !important; font-size: 12px !important;
}
.chatbot .message.bot pre {
    background: var(--m3-lowest) !important;
    border: 1px solid var(--m3-outline-variant) !important;
    border-radius: 4px !important; padding: 12px !important; overflow-x: auto !important;
}
.chatbot .message.bot pre code { color: var(--m3-on) !important; background: transparent !important; }
.chatbot .message.bot table { border-collapse: collapse !important; }
.chatbot .message.bot td, .chatbot .message.bot th { border: 1px solid var(--m3-outline-variant) !important; padding: 7px 11px !important; }
.chatbot .message.bot th { background: var(--m3-container) !important; font-family: var(--font-mono) !important; font-size: 12px !important; }
.chatbot .message.bot a { color: var(--m3-primary) !important; text-decoration: underline !important; }

.chatbot .avatar-container { width: 28px !important; height: 28px !important; }
.chatbot .avatar-container img { margin: 0 !important; padding: 0 !important; }

/* internal-step collapsibles (SHOW_AGENT_STEPS=true) */
.chatbot .message-wrap details {
    background: var(--m3-container) !important;
    border: 1px solid var(--m3-outline-variant) !important;
    font-family: var(--font-mono) !important; font-size: 12px !important;
    color: var(--m3-on-variant) !important;
}

/* progress bar */
.progress-bar { background: var(--m3-primary-container) !important; }
h1, h2, h3, h4, h5, h6 { color: #ffffff !important; font-family: var(--font) !important; }
"""
