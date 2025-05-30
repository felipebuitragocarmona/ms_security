import os
from flask import Flask, request
from app.data.database import db, migrate
from app.config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Crear carpetas si no existen
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Configurar CORS con permisos amplios
    CORS(app, supports_credentials=True)

    # Manejo explícito de solicitudes preflight
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            return '', 200

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    # Registrar Blueprints
    from app.presentation.routes.user_routes import user_bp
    from app.presentation.routes.profile_routes import profile_bp
    from app.presentation.routes.address_routes import address_bp
    from app.presentation.routes.digital_signature_routes import digital_signature_bp
    from app.presentation.routes.session_routes import session_bp
    from app.presentation.routes.password_routes import password_bp
    from app.presentation.routes.device_routes import device_bp
    from app.presentation.routes.security_question_routes import security_question_bp
    from app.presentation.routes.answer_routes import answer_bp
    from app.presentation.routes.role_routes import role_bp
    from app.presentation.routes.permission_routes import permission_bp
    from app.presentation.routes.user_role_routes import user_role_bp
    from app.presentation.routes.role_permission_routes import role_permission_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(profile_bp, url_prefix='/api/profiles')
    app.register_blueprint(address_bp, url_prefix='/api/addresses')
    app.register_blueprint(digital_signature_bp, url_prefix='/api/digital-signatures')
    app.register_blueprint(session_bp, url_prefix='/api/sessions')
    app.register_blueprint(password_bp, url_prefix='/api/passwords')
    app.register_blueprint(device_bp, url_prefix='/api/devices')
    app.register_blueprint(security_question_bp, url_prefix='/api/security-questions')
    app.register_blueprint(answer_bp, url_prefix='/api/answers')
    app.register_blueprint(role_bp, url_prefix='/api/roles')
    app.register_blueprint(permission_bp, url_prefix='/api/permissions')
    app.register_blueprint(user_role_bp, url_prefix='/api/user-roles')
    app.register_blueprint(role_permission_bp, url_prefix='/api/role-permissions')

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app
