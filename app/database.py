import sqlite3
from flask import current_app


def get_db():
    """Veritabanına bağlanır ve satırlara sütun adıyla erişim sağlar."""
    db = sqlite3.connect(current_app.config["DATABASE_URL"])
    db.row_factory = sqlite3.Row
    return db


def init_db(app):
    """leads tablosunu yoksa oluşturur."""
    with app.app_context():
        db = get_db()

        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()
        db.close()


def lead_ekle(isim, telefon, mesaj):
    """Yeni bir lead kaydeder."""
    db = get_db()

    db.execute(
        """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
        """,
        (isim, telefon, mesaj)
    )

    db.commit()
    db.close()


def tum_leadler():
    """Lead kayıtlarını yeniden eskiye doğru getirir."""
    db = get_db()

    leadler = db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY tarih DESC
        """
    ).fetchall()

    db.close()

    return [dict(lead) for lead in leadler]
    def istatistikler():
    """Toplam, bu hafta ve bugünkü kayıt sayılarını hesaplar."""
    db = get_db()

    toplam = db.execute(
        "SELECT COUNT(*) as sayi FROM leads"
    ).fetchone()["sayi"]

    bu_hafta = db.execute(
        """
        SELECT COUNT(*) as sayi FROM leads
        WHERE tarih >= datetime('now', '-7 days')
        """
    ).fetchone()["sayi"]

    bugun = db.execute(
        """
        SELECT COUNT(*) as sayi FROM leads
        WHERE date(tarih) = date('now')
        """
    ).fetchone()["sayi"]

    db.close()

    return {
        "toplam": toplam,
        "bu_hafta": bu_hafta,
        "bugun": bugun
    }
