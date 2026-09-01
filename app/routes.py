import os
from functools import wraps
from flask import Blueprint, jsonify, render_template, request, abort

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service


# Sayfa rotaları
page_bp = Blueprint("pages", __name__)


# API rotaları
api_bp = Blueprint("api", __name__)


def admin_gerekli(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        anahtar = request.headers.get("X-Admin-Key")
        if not anahtar or anahtar != os.environ.get("ADMIN_KEY"):
            abort(401)
        return f(*args, **kwargs)
    return wrapper


@page_bp.route("/")
def index():
    return render_template("index.html")


@page_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json(silent=True) or {}

    mesaj = data.get("mesaj")
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj alanı zorunludur."
        }), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            "basari": True,
            "cevap": cevap
        })

    except AIServiceError as error:
        return jsonify({
            "basari": False,
            "hata": str(error)
        }), 503


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    data = request.get_json(silent=True) or {}

    isim = data.get("isim")
    telefon = data.get("telefon")
    mesaj = data.get("mesaj", "")

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "İsim ve telefon alanları zorunludur."
        }), 400

    try:
        lead_ekle(isim, telefon, mesaj)

        return jsonify({
            "basari": True,
            "mesaj": "İletişim bilgileriniz başarıyla kaydedildi."
        }), 201

    except Exception:
        return jsonify({
            "basari": False,
            "hata": "Kayıt sırasında bir hata oluştu."
        }), 500


@api_bp.route("/leads", methods=["GET"])
@admin_gerekli
def leadleri_getir():
    try:
        leadler = tum_leadler()

        return jsonify({
            "basari": True,
            "leadler": leadler
        })

    except Exception:
        return jsonify({
            "basari": False,
            "hata": "Lead kayıtları alınamadı."
        }), 500
