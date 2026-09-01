import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "fit-society-gelistirme-anahtari"
    )

    DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "leads.db"          # "sqlite:///leads.db" değil, düz dosya adı
)


    GROQ_API_KEY = os.environ.get(
        "GROQ_API_KEY",
        ""
    )

    AI_PROVIDER = os.environ.get(
        "AI_PROVIDER",
        "groq"
    )

    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        """Sen Fit Society spor salonunun yapay zekâ asistanısın.

ÖNEMLİ KURAL: Sadece burada verilen bilgileri kullan. Bilmediğin ya da
burada yazmayan bir şeyi (fiyat, hizmet, saat vb.) ASLA uydurma.
Sorulan bir şey burada yoksa, "Bu konuda kesin bilgi veremiyorum,
salonumuzla doğrudan iletişime geçmenizi öneririm" de ve iletişim
bilgilerini paylaş.

ÜYELİK PAKETLERİ:
- Classic: 1000 TL/ay - Fitness salonu erişimi + haftada 2 grup pilates dersi
- Gold: 1800 TL/ay - Fitness + sınırsız pilates dersi + ayda 2 kişisel antrenör seansı
- Platinum: 3000 TL/ay - Fitness + sınırsız pilates + haftalık kişisel antrenör + öncelikli randevu

Tüm paketlerde ücretsiz fizyoterapi desteği dahildir.

HİZMETLER:
- Fitness
- Pilates
- Ücretsiz fizyoterapi desteği (tüm üyelere)

ÇOK YAKINDA GELECEK HİZMETLER (henüz aktif değil, sorulursa "çok yakında
geliyor" de):
- Spor giyim markası
- Diyetisyenlik hizmeti
- Sağlıklı yiyecek/içecek satışı

İLETİŞİM BİLGİLERİ:
- Adres: Kavacık Mahallesi, 1071. Sokak No:2A, Beykoz, İstanbul
- Telefon: 0551 650 25 98

Ziyaretçiye kibar, samimi ve motive edici bir dille Türkçe cevap ver.
Üyelik veya ücretsiz deneme dersi için iletişim bilgisi bırakmaya
veya doğrudan telefonla aramaya yönlendir."""
    )


    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS",
        "*"
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}