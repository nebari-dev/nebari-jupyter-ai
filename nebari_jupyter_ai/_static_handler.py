from jupyter_server.utils import url_path_join
from tornado.web import StaticFileHandler
import os

from nebari_jupyter_ai.persona import NEBARI_ASSISTANT_PERSONA

NEBARI_ASSISTANT_AVATAR_ICON_PATH = str(os.path.join(os.path.dirname(__file__), "static", "nebari-logo-with-bg.svg"))

def setup_handlers(web_app):
    host_pattern = ".*$"    
        
    # Get the base_url from the web_app  settings
    base_url = web_app.settings.get('base_url', '/')
    print('=' * 80)
    print(f"base_url: {base_url}")
    print('=' * 80)

    handlers = [(
        rf"{url_path_join(base_url, NEBARI_ASSISTANT_PERSONA.avatar_route)}()", # the `()` at the end of the URL denotes an empty regex capture group
        StaticFileHandler, 
        {"path": NEBARI_ASSISTANT_AVATAR_ICON_PATH}
    )]
    web_app.add_handlers(host_pattern, handlers)


if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    print(os.path.join(base_path, "static"))
