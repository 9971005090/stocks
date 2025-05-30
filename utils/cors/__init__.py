from flask_cors import CORS

__all__ = ['SETUP']

def SETUP(app):
    CORS(app, resources={r"/api/*": {"origins": "*"}})