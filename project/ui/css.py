custom_css = """
    /* Minimal, quiet light theme. No decoration - just readable. */
    .gradio-container {
        max-width: 940px !important;
        margin: 0 auto !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 15px !important;
        background: #fbfbfa !important;
        color: #24252a !important;
    }
    .gradio-container p, .gradio-container li, .gradio-container span, .gradio-container label {
        color: #24252a !important;
    }
    footer { display: none !important; }
    .progress-text { display: none !important; }
    * { box-shadow: none !important; }

    h1, h2, h3, h4 { color: #1a1b1f !important; font-weight: 600 !important; }
    .gradio-container h2 { font-size: 19px !important; margin: 4px 0 2px 0 !important; }
    .app-intro { color: #6b6c72 !important; font-size: 14px !important; margin: 0 0 4px 0 !important; }

    /* Tabs */
    .tab-nav { border-bottom: 1px solid #e6e6e3 !important; margin-bottom: 8px !important; }
    .tab-nav button {
        color: #6b6c72 !important; background: transparent !important;
        border: none !important; border-bottom: 2px solid transparent !important;
        border-radius: 0 !important; font-size: 14px !important; font-weight: 500 !important;
        padding: 9px 14px !important;
    }
    .tab-nav button:hover { color: #24252a !important; }
    .tab-nav button.selected { color: #1a1b1f !important; border-bottom: 2px solid #4a6da7 !important; }

    /* Blocks */
    .block, .form { background: transparent !important; border: none !important; }
    .gradio-container label, .block-label {
        font-size: 13px !important; font-weight: 500 !important; color: #6b6c72 !important;
        text-transform: none !important; letter-spacing: 0 !important;
    }

    /* Inputs */
    input, textarea, .file-preview, [data-testid="file-upload"], #file-list-box {
        background: #ffffff !important;
        border: 1px solid #dededa !important;
        border-radius: 8px !important;
        color: #24252a !important;
        font-size: 15px !important;
    }
    input::placeholder, textarea::placeholder { color: #9a9b9f !important; }
    input:focus, textarea:focus { border-color: #4a6da7 !important; outline: none !important; }
    [data-testid="file-upload"], .file-preview { min-height: 170px !important; }
    [data-testid="file-upload"] *, .file-preview * { color: #6b6c72 !important; }
    #file-list-box, #file-list-box textarea { font-size: 14px !important; background: #ffffff !important; }

    /* Buttons */
    button.primary, button.secondary, button.stop {
        border-radius: 8px !important; font-weight: 600 !important; font-size: 14px !important;
        border: 1px solid transparent !important;
    }
    button.primary { background: #4a6da7 !important; color: #ffffff !important; }
    button.primary:hover { background: #3f5f95 !important; }
    button.secondary { background: #ffffff !important; color: #24252a !important; border-color: #dededa !important; }
    button.secondary:hover { background: #f4f4f2 !important; }
    button.stop { background: #ffffff !important; color: #b23b34 !important; border-color: #e6c9c6 !important; }
    button.stop:hover { background: #fbf1f0 !important; }

    /* Accordion */
    .gradio-container details, .accordion {
        background: #ffffff !important; border: 1px solid #e6e6e3 !important; border-radius: 8px !important;
    }
    .gradio-container details summary { color: #6b6c72 !important; font-size: 14px !important; }

    /* Chat */
    .chatbot, .chatbot .message-wrap {
        background: #ffffff !important; border: 1px solid #e6e6e3 !important; border-radius: 10px !important;
    }
    .chatbot .message-wrap > div { padding: 16px !important; gap: 14px !important; }
    .chatbot .message, .chatbot .message p, .chatbot .message li {
        font-size: 15px !important; line-height: 1.7 !important;
    }
    .chatbot .message p { margin: 0 0 10px 0 !important; }
    .chatbot .message p:last-child { margin-bottom: 0 !important; }
    .chatbot .message.user, .chatbot .bubble.user {
        background: #eef1f6 !important; color: #24252a !important; border: none !important;
        border-radius: 10px !important; padding: 10px 14px !important;
    }
    .chatbot .message.bot, .chatbot .bubble.bot {
        background: #fbfbfa !important; color: #24252a !important;
        border: 1px solid #e6e6e3 !important; border-radius: 10px !important;
        max-width: 100% !important; padding: 14px 16px !important;
    }
    .chatbot .message.bot h1, .chatbot .message.bot h2,
    .chatbot .message.bot h3, .chatbot .message.bot h4 {
        font-size: 15px !important; font-weight: 600 !important; margin: 2px 0 10px 0 !important;
    }
    .chatbot .message.bot hr { border: none !important; border-top: 1px solid #e6e6e3 !important; margin: 2px 0 12px 0 !important; }
    .chatbot .message.bot blockquote {
        margin: 2px 0 0 0 !important; padding: 12px 14px !important;
        background: #f4f6f9 !important; border-left: 3px solid #4a6da7 !important;
        border-radius: 6px !important; color: #24252a !important;
    }
    .chatbot .message.bot blockquote p { margin: 0 !important; }
    .chatbot .message.bot code {
        background: #f1f1ef !important; color: #8a4b2f !important;
        padding: 2px 5px !important; border-radius: 4px !important; font-size: 13px !important;
    }
    .chatbot .message.bot pre {
        background: #f6f6f4 !important; border: 1px solid #e6e6e3 !important;
        border-radius: 8px !important; padding: 12px !important; overflow-x: auto !important;
    }
    .chatbot .message.bot pre code { color: #24252a !important; background: transparent !important; }
    .chatbot .message.bot table { border-collapse: collapse !important; }
    .chatbot .message.bot td, .chatbot .message.bot th { border: 1px solid #e6e6e3 !important; padding: 7px 11px !important; }
    .chatbot .message.bot a { color: #4a6da7 !important; text-decoration: underline !important; }
    .chatbot .avatar-container { display: none !important; }

    .chatbot .message-wrap details {
        background: #f6f6f4 !important; border: 1px solid #e6e6e3 !important;
        font-size: 13px !important; color: #6b6c72 !important;
    }
    .progress-bar { background: #4a6da7 !important; }
"""
