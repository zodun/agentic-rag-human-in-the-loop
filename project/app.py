import sys
import os
import logging

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Suppress OTel "Failed to detach context" warning caused by generator/context interaction.
# Tracing is unaffected.
# Known bug: https://github.com/open-telemetry/opentelemetry-python/issues/2606
class _SuppressOtelDetachWarning(logging.Filter):
    def filter(self, record):
        return "Failed to detach context" not in record.getMessage()

logging.getLogger("opentelemetry.context").addFilter(_SuppressOtelDetachWarning())

from ui.css import custom_css
from ui.gradio_app import create_gradio_ui

# The custom CSS is a light palette; force Gradio's own light mode so every
# built-in element matches regardless of the viewer's OS setting.
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
    demo.launch(css=custom_css, js=FORCE_LIGHT_JS)