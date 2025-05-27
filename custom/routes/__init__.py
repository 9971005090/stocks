from .stocks import STOCKS_BLUEPRINT

def INIT_BLUEPRINT(app):
    app.register_blueprint(STOCKS_BLUEPRINT, url_prefix='/API')