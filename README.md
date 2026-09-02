# fit_society
# Fit Society - AI Destekli Web Sistemi

Fit Society spor salonu için geliştirilen, yapay zeka destekli chatbot ve yönetim paneli içeren backend sistemi. Wix üzerinde barındırılan ana site ile Render'da çalışan bu Flask uygulaması Velo (JavaScript) aracılığıyla entegre edilmiştir.

## Özellikler

- 🤖 **AI Chatbot**: Groq API (openai/gpt-oss-20b modeli) ile çalışan, salon hizmetleri ve üyelik paketleri hakkında bilgi veren sohbet asistanı
- 📝 **Lead Kayıt Sistemi**: Ziyaretçilerin ücretsiz deneme dersi için iletişim bilgilerini bıraktığı form
- 📊 **Yönetim Paneli (Dashboard)**: Admin-key korumalı, kayıt istatistikleri (toplam/haftalık/günlük) ve lead listesini gösteren panel
- 🔒 **Güvenlik**: CORS kısıtlaması ve admin anahtarı ile korunan hassas endpoint'ler

## Teknoloji Yığını

- **Backend**: Python, Flask
- **Veritabanı**: SQLite
- **AI**: Groq API
- **Deployment**: Render
- **Frontend Entegrasyonu**: Wix + Velo (JavaScript)

## Frontend Entegrasyonu

Bu proje iki farklı arayüz sunar:

1. **Flask HTML Şablonları** (`templates/index.html`, `templates/dashboard.html`):
   Render adresine doğrudan erişimde çalışan, geliştirme/test amaçlı sayfalar.

2. **Wix + Velo Entegrasyonu** (asıl canlı sistem):
   Gerçek kullanıcıya sunulan arayüz Wix'te tasarlanmış, Velo (JavaScript)
   koduyla bu Flask API'sine `fetch()` istekleri atarak veri alışverişi yapar.
   - **Chatbot**: Wix sayfasındaki konteyner içine yerleştirilmiş Text/Input/Button
     elementleri, Velo koduyla `/sohbet` endpoint'ine bağlanır.
   - **Dashboard**: Wix Repeater elementi, Velo koduyla `/leads` ve
     `/istatistikler` endpoint'lerinden veri çekip listeler.
   - **İletişim Formu**: Wix Input elementleri, Velo koduyla `/leads`
     endpoint'ine POST isteği atar.

## Proje Yapısı

```
fit_society/
├── app/
│   ├── __init__.py          # Flask uygulama fabrikası
│   ├── database.py          # Veritabanı işlemleri
│   ├── routes.py            # API ve sayfa route'ları
│   ├── services/
│   │   └── ai_service.py    # Groq API entegrasyonu
│   └── templates/
│       ├── index.html       # Chatbot + kayıt formu (test amaçlı)
│       └── dashboard.html   # Yönetim paneli (test amaçlı)
├── config.py                 # Ortam değişkenleri ve ayarlar
├── requirements.txt
├── run.py                    # Uygulama başlatıcı
└── README.md
```

## Kurulum

1. Repoyu klonla:
   ```bash
   git clone <repo-url>
   cd fit_society
   ```

2. Gerekli paketleri yükle:
   ```bash
   pip install -r requirements.txt
   ```

3. `.env` dosyası oluştur ve gerekli değişkenleri tanımla (aşağıdaki tabloya bak)

4. Uygulamayı çalıştır:
   ```bash
   python run.py
   ```

## Ortam Değişkenleri

| Değişken | Açıklama |
|---|---|
| `SECRET_KEY` | Flask oturum güvenliği için gizli anahtar |
| `DATABASE_URL` | SQLite veritabanı dosya adı (örn. `leads.db`) |
| `GROQ_API_KEY` | Groq API erişim anahtarı |
| `BUSINESS_CONTEXT` | Chatbot'un kullandığı işletme bilgisi metni |
| `CORS_ORIGINS` | İzin verilen frontend domain adresi (Wix site adresi) |
| `ADMIN_KEY` | Dashboard ve lead verilerine erişim için admin şifresi |

## API Endpoint'leri

| Method | Endpoint | Açıklama | Yetki |
|---|---|---|---|
| GET | `/` | Ana sayfa (chatbot + form) | Herkese açık |
| GET | `/dashboard` | Yönetim paneli sayfası | Herkese açık (içerik admin-key ile korunur) |
| POST | `/sohbet` | Chatbot'a mesaj gönderme | Herkese açık |
| POST | `/leads` | Yeni kayıt oluşturma | Herkese açık |
| GET | `/leads` | Tüm kayıtları listeleme | Admin-key gerekli |
| GET | `/istatistikler` | Kayıt istatistikleri | Admin-key gerekli |

## Dağıtım (Deployment)

Bu proje Render üzerinde barındırılmaktadır. Ortam değişkenleri Render'ın Environment sekmesinden yönetilir. `main` dalına yapılan her push, otomatik olarak yeniden dağıtımı (deploy) tetikler.

## Bilinen Sınırlamalar

- SQLite veritabanı Render'ın ücretsiz planında kalıcı değildir; disk sıfırlanabilir
- Ücretsiz Render planında 15 dakika hareketsizlik sonrası servis uykuya geçer, ilk istek 50+ saniye gecikebilir
