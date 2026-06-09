from flask import Flask
from src.configs import Mode, configs
from src.routers import blueprints
from src.extensions import extensions

def create_app(mode: Mode) -> Flask:
    app = Flask(f'{mode}_app')
    app.config.from_object(configs[mode])
    for bp in blueprints:
        app.register_blueprint(bp)
    for ext in extensions:
        ext.init_app(app)
    return app
