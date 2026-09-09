import sys
import os
import logging

sys.path.insert(0, os.path.dirname(__file__))

# Keep embedding + tokenizer work off Apple's MPS backend, which crashes
# sentence-transformers under load with a Metal command-buffer assertion.
os.environ.setdefault("EMBEDDING_DEVICE", "cpu")
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Suppress OTel "Failed to detach context" warning caused by generator/context interaction.
# Tracing is unaffected.
# Known bug: https://github.com/open-telemetry/opentelemetry-python/issues/2606
class _SuppressOtelDetachWarning(logging.Filter):
    def filter(self, record):
        return "Failed to detach context" not in record.getMessage()

logging.getLogger("opentelemetry.context").addFilter(_SuppressOtelDetachWarning())

import gradio as gr

from ui.css import custom_css
from ui.gradio_app import create_gradio_ui

# A polished built-in Gradio theme does the visual work; custom_css only nudges it.
THEME = gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    radius_size="md",
)

# Force Gradio's light mode so it looks the same regardless of the viewer's OS setting.
FORCE_LIGHT_JS = """
function () {
    const u = new URL(window.location);
    if (u.searchParams.get('__theme') !== 'light') {
        u.searchParams.set('__theme', 'light');
        window.location.replace(u.toString());
    }
}
"""

if __name__ == "__main__":
    print("\n🔨 Creating RAG Assistant...")
    demo = create_gradio_ui()
    print("\n🚀 Launching RAG Assistant...")
    demo.launch(css=custom_css, js=FORCE_LIGHT_JS, theme=THEME)