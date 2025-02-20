from tornado.web import StaticFileHandler
import os

from nebari_jupyter_ai.persona import NEBARI_ASSISTANT_PERSONA

NEBARI_ASSISTANT_AVATAR_ICON_PATH = str(os.path.join(os.path.dirname(__file__), "static", "nebari-logo-with-bg.svg"))

def setup_handlers(web_app):
    host_pattern = ".*$"    
    
    handlers = [(
        rf"{NEBARI_ASSISTANT_PERSONA.avatar_route}()", # the `()` at the end of the URL denotes an empty regex capture group
        StaticFileHandler, 
        {"path": NEBARI_ASSISTANT_AVATAR_ICON_PATH}
    )]
    print('='*50)
    print(handlers)
    print('='*50)
    web_app.add_handlers(host_pattern, handlers)

    
if __name__ == "__main__":
        base_path = os.path.dirname(__file__)
        print(os.path.join(base_path, "static"))
        