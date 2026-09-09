custom_css = """
    /* ============================================================
       Calm light theme - low eye strain, high legibility.
       bg #f5f6f8 | surface #ffffff | text #24292f | accent #3b6fb6
       ============================================================ */
    .gradio-container {
        max-width: 1120px !important;
        width: 100% !important;
        margin: 0 auto !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-size: 16px !important;
        background: #f5f6f8 !important;
        color: #24292f !important;
    }
    .gradio-container p, .gradio-container li, .gradio-container span,
    .gradio-container label, .gradio-container h1, .gradio-container h2, .gradio-container h3 {
        color: #24292f !important;
    }

    #doc-management-tab { max-width: 600px !important; margin: 0 auto !important; }
    footer { display: none !important; }
    .progress-text { display: none !important; }

    /* ---------------- Tabs ---------------- */
    .tab-nav { border-bottom: 1px solid #d8dbe0 !important; }
    button[role="tab"] {
        color: #57606a !important;
        background: transparent !important;
        border-bottom: 3px solid transparent !important;
        border-radius: 0 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        padding: 10px 16px !important;
    }
    button[role="tab"]:hover { color: #24292f !important; }
    button[role="tab"][aria-selected="true"] {
        color: #1f2328 !important;
        border-bottom: 3px solid #3b6fb6 !important;
    }

    /* ---------------- Buttons ---------------- */
    button { border-radius: 8px !important; font-weight: 700 !important; box-shadow: none !important; }
    .primary { background: #3b6fb6 !important; color: #fff !important; font-size: 15px !important; }
    .primary:hover { background: #335f9e !important; }
    .stop { background: #c4453f !important; color: #fff !important; }
    .stop:hover { background: #ad3b36 !important; }

    /* ---------------- Inputs ---------------- */
    input, textarea, .file-preview, [data-testid="file-upload"], #file-list-box {
        background: #ffffff !important;
        border: 1px solid #ced2d9 !important;
        border-radius: 10px !important;
        color: #24292f !important;
        font-size: 16px !important;
    }
    input::placeholder, textarea::placeholder { color: #8b939e !important; }
    input:focus, textarea:focus { border-color: #3b6fb6 !important; outline: none !important; }
    [data-testid="file-upload"], .file-preview { min-height: 190px !important; }
    [data-testid="file-upload"] *, .file-preview * { color: #57606a !important; }
    #file-list-box textarea { background: transparent !important; border: none !important; }

    /* ============================================================
       CHAT
       ============================================================ */
    .chatbot, .chatbot .message-wrap {
        background: #ffffff !important;
        border: 1px solid #dfe1e6 !important;
        border-radius: 12px !important;
    }
    .chatbot .message-wrap > div { padding: 18px !important; gap: 16px !important; }
    .chatbot .message-row { margin-bottom: 6px !important; }

    /* ---- message text ---- */
    .chatbot .message,
    .chatbot .message p,
    .chatbot .message li,
    .chatbot .message td,
    .chatbot .message th {
        font-size: 16px !important;
        line-height: 1.72 !important;
    }
    .chatbot .message p  { margin: 0 0 12px 0 !important; }
    .chatbot .message p:last-child { margin-bottom: 0 !important; }
    .chatbot .message ul, .chatbot .message ol { margin: 8px 0 12px 0 !important; padding-left: 22px !important; }
    .chatbot .message li { margin: 4px 0 !important; }

    .chatbot .message.user, .chatbot .bubble.user {
        background: #e7f0fb !important;
        color: #1f2937 !important;
        border: 1px solid #cfe0f5 !important;
        font-weight: 500 !important;
        padding: 12px 16px !important;
    }
    .chatbot .message.bot, .chatbot .bubble.bot {
        background: #f7f8fa !important;
        color: #24292f !important;
        border: 1px solid #dfe1e6 !important;
        max-width: 100% !important;
        padding: 16px 18px !important;
    }
    .chatbot .message.bot strong, .chatbot .message.bot b { color: #1f2328 !important; font-weight: 700 !important; }

    /* divider + heading before the drafted reply */
    .chatbot .message.bot h1, .chatbot .message.bot h2,
    .chatbot .message.bot h3, .chatbot .message.bot h4 {
        color: #1f2328 !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        margin: 2px 0 12px 0 !important;
    }
    .chatbot .message.bot hr {
        border: none !important;
        border-top: 2px solid #d8dbe0 !important;
        margin: 2px 0 14px 0 !important;
    }

    /* approval prompt / receipts (sent as blockquotes) -> calm callout */
    .chatbot .message.bot blockquote {
        margin: 2px 0 0 0 !important;
        padding: 14px 16px !important;
        background: #eef4fb !important;
        border-left: 4px solid #3b6fb6 !important;
        border-radius: 8px !important;
        color: #1f2328 !important;
        font-size: 16px !important;
    }
    .chatbot .message.bot blockquote p { margin: 0 !important; color: #1f2328 !important; }

    /* code + tables */
    .chatbot .message.bot code {
        background: #eef0f3 !important;
        color: #9a3412 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-size: 14px !important;
    }
    .chatbot .message.bot pre {
        background: #f2f3f5 !important;
        border: 1px solid #dfe1e6 !important;
        border-radius: 8px !important;
        padding: 14px !important;
        overflow-x: auto !important;
    }
    .chatbot .message.bot pre code { color: #24292f !important; background: transparent !important; }
    .chatbot .message.bot table { border-collapse: collapse !important; margin: 8px 0 !important; }
    .chatbot .message.bot td, .chatbot .message.bot th {
        border: 1px solid #d8dbe0 !important;
        padding: 8px 12px !important;
    }
    .chatbot .message.bot th { background: #f2f3f5 !important; }
    .chatbot .message.bot a { color: #3b6fb6 !important; text-decoration: underline !important; }

    /* collapsible internal-step rows (SHOW_AGENT_STEPS=true only) */
    .chatbot .message-wrap details {
        background: #f2f3f5 !important;
        border: 1px solid #dfe1e6 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        color: #57606a !important;
    }

    .chatbot .avatar-container img, .message-row img { margin: 0 !important; padding: 0 !important; }
    .chatbot .avatar-container { width: 30px !important; height: 30px !important; }
    form:has(textarea) textarea { font-size: 16px !important; }

    /* ---------------- Misc ---------------- */
    h1, h2, h3, h4, h5, h6 { color: #1f2328 !important; }
    .prose, .prose * { color: #57606a !important; }
    .progress-bar { background: #3b6fb6 !important; }
    * { box-shadow: none !important; }
"""
