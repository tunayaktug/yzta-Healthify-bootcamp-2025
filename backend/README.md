# Healtify - Backend

Bu klasör, Healtify projesinin FastAPI ile geliştirilen backend tarafını içerir.

## Kullanılan Teknolojiler
- FastAPI
- SQLAlchemy (ORM)
- MSSQL (Veritabanı)
- Passlib (bcrypt ile şifreleme)
- Pydantic (veri doğrulama)
- Uvicorn (ASGI sunucusu)

## Kurulum ve Çalıştırma

```bash
# 1. Sanal ortam oluştur
python -m venv .venv

# 2. Sanal ortamı aktifleştir
.venv\Scripts\activate  # Windows için
source .venv/bin/activate  #  Mac/Linux

# 3. Gerekli kütüphaneleri yükle
pip install -r requirements.txt

# 4. Uygulamayı çalıştır
uvicorn backend.main:app --reload
Not: Komutu çalıştırmadan önce projenin kök dizininde olduğunuzdan emin olun.



backend/
├── database/       # Veritabanı bağlantısı
├── models/         # Veritabanı modelleri
├── routers/        # API endpointleri
├── utils/          # Yardımcı fonksiyonlar
├── main.py         # Uygulama giriş noktası
├── requirements.txt
└── README.md

Not: Veritabanı bağlantısı MSSQL kullanılarak ODBC Driver 17 ile yapılmıştır.