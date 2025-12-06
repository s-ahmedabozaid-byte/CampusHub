from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager
from .models import user_model, event_model

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints (imports inside to avoid circular dependencies)
    from .controllers.auth_controller import auth_bp
    from .controllers.user_controller import user_bp
    from .controllers.main_controller import main_bp
    from .controllers.event_controller import event_bp
    from .controllers.admin_controller import admin_bp
    from .controllers.announcement_controller import announcement_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(main_bp)
    app.register_blueprint(event_bp, url_prefix='/events')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(announcement_bp)

    return app
