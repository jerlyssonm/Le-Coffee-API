from flask import Flask
# importar as bp
from app.routes.admin_blueprint import bp_admin

def init_app(app: Flask):
    # app.register_blueprint(nome da bp)
    app.register_blueprint(bp_admin)
    ...