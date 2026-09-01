from flask import Flask
from flask_cors import CORS

from config import DevelopmentConfig
from app.database import init_db
from app.routes import page_bp, api_bp


def create_app():
    """Flask uygulamasını oluşturur ve yapılandırır."""

    app = Flask(__name__)

    # Geliştirme ayarlarını yükle.
    app.config.from_object(DevelopmentConfig)

    # Wix bağlantısı için CORS'u etkinleştir.
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # Veritabanını oluştur.
    with app.app_context():
        init_db(app)

    # Sayfa ve API blueprint'lerini kaydet.
    app.register_blueprint(page_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/health")
    def health():
        return {
            "basari": True,
            "durum": "healthy"
        }

    return app