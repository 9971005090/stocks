from flask_cors import CORS

__all__ = [' st']

def SETUP(app):
    CORS(app, resources={r"/api/*": {"origins": "*"}})