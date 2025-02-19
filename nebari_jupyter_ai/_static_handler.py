from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
from tornado.web import StaticFileHandler
import os

class StaticFileHandler(ExtensionHandlerMixin, StaticFileHandler):
    pass

def setup_handlers(web_app):
    host_pattern = ".*$"
    base_path = os.path.dirname(__file__)
    
    handlers = [(
        r"/nebari-jupyter-ai/static/(.*)", 
        StaticFileHandler, 
        {"path": os.path.join(base_path, "static")}
    )]
    web_app.add_handlers(host_pattern, handlers)