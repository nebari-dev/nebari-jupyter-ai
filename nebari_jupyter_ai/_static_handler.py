from tornado.web import StaticFileHandler
import os

def setup_handlers(web_app):
    host_pattern = ".*$"
    base_path = os.path.dirname(__file__)
    
    handlers = [(
        r"nebari-jupyter-ai/static/(.*)", 
        StaticFileHandler, 
        {"path": os.path.join(base_path, "static")}
    )]
    web_app.add_handlers(host_pattern, handlers)

    
if __name__ == "__main__":
        base_path = os.path.dirname(__file__)
        print(os.path.join(base_path, "static"))
        