# Telegramda Matematika Test Boti

Turli qiyinlikdagi 10 ta matematik savol bilan test o'tkazuvchi Telegram bot.

## Tavsif

Bot har safar yangi savollar bilan interaktiv matematik test o'tkazadi. Test uch xil qiyinlik darajasidagi 10 ta savoldan iborat:
- **Oson** (3 ta savol): oddiy qo'shish va ayirish
- **O'rta** (4 ta savol): ko'paytirish va bo'lish
- **Qiyin** (3 ta savol): darajalar, tenglamalar, mantiqiy masalalar

## Imkoniyatlar

- ✅ Har safar yangi dinamik savollar
- ✅ Boshlashda 3 ta Reply tugma
- ✅ Har bir savol uchun 4 ta javob varianti bilan Inline klaviatura
- ✅ Har bir javobdan keyin pop-up xabar (to'g'ri/noto'g'ri)
- ✅ Foiz bilan natijalarni hisoblash
- ✅ Natijalarga qarab shaxsiylashtirilgan xabarlar
- ✅ Yordam va bot haqida ma'lumot
- ✅ Barcha so'rovlarni asinxron qayta ishlash

## Texnologiyalar

- Python 3.8+
- aiogram 3.24
- python-dotenv

## O'rnatish

### 1. Fayllarni yuklab oling

### 2. Virtual muhit yarating (tavsiya etiladi)

```bash
python -m venv venv
```

### 3. Virtual muhitni faollashtiring

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Bog'liqliklarni o'rnating

```bash
pip install -r requirements.txt
```

### 5. `.env` faylini yarating

`.env.example` faylini `.env` ga nusxalang:
```bash
copy .env.example .env
```

### 6. Bot tokenini oling

1. Telegramda [@BotFather](https://t.me/botfather) ni toping
2. `/newbot` buyrug'ini yuboring
3. Bot yaratish bo'yicha ko'rsatmalarga amal qiling
4. Olingan tokenni nusxalang

### 7. Tokenni sozlang

`.env` faylini oching va tokeningizni qo'ying:
```
BOT_TOKEN=sizning_tokeningiz
```

## Ishga tushirish

Botni quyidagi buyruq bilan ishga tushiring:

```bash
python math_bot.py
```

Quyidagi xabarni ko'rishingiz kerak:
```
INFO:__main__:Bot ishga tushmoqda...
```

## 📱 Foydalanish

1. Telegramda botingizni toping
2. `/start` buyrug'ini yuboring
3. Harakatni tanlang:
   - **📝 Testni boshlash** - testni boshlash
   - **❓ Yordam** - ko'rsatma olish
   - **👤 Muallif haqida** - bot haqida ma'lumot

### Buyruqlar

- `/start` - asosiy menyuni ko'rsatish
- `/test` - testni boshlash

## Test qanday ishlaydi

1. "Testni boshlash" tugmasini bosganingizdan keyin bot birinchi savolni yuboradi
2. Har bir savol ostida 4 ta javob varianti bilan tugmalar
3. Javob tanlaganingizdan keyin pop-up xabar paydo bo'ladi:
   - ✅ "To'g'ri!" - agar javob to'g'ri bo'lsa
   - ❌ "Noto'g'ri! To'g'ri javob: X" - agar javob noto'g'ri bo'lsa
4. Keyingi savol avtomatik yuklanadi
5. 10-savoldan keyin natijalar ko'rsatiladi:
   - To'g'ri javoblar soni
   - To'g'ri javoblar foizi
   - Shaxsiylashtirilgan xabar

## Dinamik savollar

**Yangi xususiyat!** Har safar test boshlanganda yangi tasodifiy savollar yaratiladi:

- **Oson savollar**: 1 dan 100 gacha sonlar bilan qo'shish va ayirish
- **O'rta savollar**: 2 dan 15 gacha sonlar bilan ko'paytirish va bo'lish
- **Qiyin savollar**: 
  - Darajalar (masalan: 2³ + 5²)
  - Tenglamalar (masalan: x + 15 = 42)
  - Murakkab amallar (masalan: (12 + 8) × 3 - 10)

Bu har bir test noyob va qiziqarli bo'lishini ta'minlaydi!

## Baholash tizimi

- **100%** - 🏆 Matematika dahosi!
- **80-99%** - 🎉 A'lo!
- **60-79%** - 👍 Yaxshi!
- **40-59%** - 📖 Yomon emas!
- **0-39%** - 💪 Mashq sizni kuchli qiladi!

## Loyiha tuzilmasi

```
.
├── math_bot.py          # Asosiy bot fayli
├── config.py            # Konfiguratsiya (token yuklash)
├── requirements.txt     # Bog'liqliklar
├── .env.example        # Muhit o'zgaruvchilari uchun shablon
├── .env               # Sizning muhit o'zgaruvchilaringiz (qo'lda yaratiladi)
└── README.md          # Ushbu fayl
```

## Muammolarni hal qilish

### Bot ishga tushmaydi
- `.env` faylida token to'g'ri ko'rsatilganligini tekshiring
- Barcha bog'liqliklar o'rnatilganligiga ishonch hosil qiling
- Python versiyasini tekshiring (3.8+ kerak)

### Bot javob bermaydi
- Bot ishga tushganligiga ishonch hosil qiling
- Internet aloqasini tekshiring
- Xatolar uchun loglarni tekshiring

## Litsenziya

Ushbu loyiha ta'lim maqsadlarida yaratilgan va erkin foydalanish uchun ochiq.