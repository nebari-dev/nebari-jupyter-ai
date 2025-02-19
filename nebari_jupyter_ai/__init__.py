import jupyter_server.serverapp
from ._version import __version__
from ._static_handler import setup_handlers

def _jupyter_server_extension_points():
    return [{
        "module": "nebari_jupyter_ai"
    }]

def load_jupyter_server_extension(nb_server_app: jupyter_server.serverapp.ServerApp):
    # This function is called when the extension is loaded.
    setup_handlers(nb_server_app.web_app)

    