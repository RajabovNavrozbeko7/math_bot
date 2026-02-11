"""
Telegram Matematika Test Boti
10 ta turli qiyinlikdagi matematik savollar bilan test o'tkazuvchi bot

aiogram 3.24 yordamida Telegram Bot API bilan ishlaydi
"""

import asyncio
import logging
import random
from typing import Dict, List, Tuple
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters.callback_data import CallbackData

# Muhit o'zgaruvchilarini yuklash
load_dotenv()

# Konfiguratsiyani import qilish
import config

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot va dispetcherni ishga tushirish
BOT_TOKEN = config.TOKEN
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN muhit o'zgaruvchilarida topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============================================================================
# CALLBACK UCHUN MA'LUMOTLAR STRUKTURASI
# ============================================================================

class QuestionCallback(CallbackData, prefix="quiz"):
    """Savollarga javoblar uchun callback ma'lumotlari"""
    question_id: int
    answer_id: int
    is_correct: bool


# ============================================================================
# DINAMIK SAVOLLAR GENERATORI
# ============================================================================

def generate_easy_question(question_num: int) -> dict:
    """Oson savol yaratish (qo'shish, ayirish)"""
    operation = random.choice(['+', '-'])
    
    if operation == '+':
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        correct_answer = a + b
        question_text = f"{a} + {b}"
    else:  # ayirish
        a = random.randint(10, 100)
        b = random.randint(1, a - 1)
        correct_answer = a - b
        question_text = f"{a} - {b}"
    
    # Noto'g'ri javoblar yaratish
    wrong_answers = []
    while len(wrong_answers) < 3:
        offset = random.randint(-10, 10)
        if offset == 0:
            continue
        wrong = correct_answer + offset
        if wrong > 0 and wrong not in wrong_answers and wrong != correct_answer:
            wrong_answers.append(wrong)
    
    # Javoblarni aralashtirib qo'yish
    answers = [correct_answer] + wrong_answers
    random.shuffle(answers)
    correct_index = answers.index(correct_answer)
    
    return {
        "id": question_num,
        "question": f"❓ Savol {question_num + 1}/10 (Oson)\n\n{question_text} = ?",
        "answers": [str(ans) for ans in answers],
        "correct": correct_index
    }


def generate_medium_question(question_num: int) -> dict:
    """O'rta qiyinlikdagi savol yaratish (ko'paytirish, bo'lish)"""
    operation = random.choice(['*', '/'])
    
    if operation == '*':
        a = random.randint(2, 15)
        b = random.randint(2, 15)
        correct_answer = a * b
        question_text = f"{a} × {b}"
    else:  # bo'lish
        b = random.randint(2, 12)
        quotient = random.randint(2, 20)
        a = b * quotient
        correct_answer = quotient
        question_text = f"{a} ÷ {b}"
    
    # Noto'g'ri javoblar yaratish
    wrong_answers = []
    while len(wrong_answers) < 3:
        offset = random.randint(-5, 5)
        if offset == 0:
            continue
        wrong = correct_answer + offset
        if wrong > 0 and wrong not in wrong_answers and wrong != correct_answer:
            wrong_answers.append(wrong)
    
    # Javoblarni aralashtirib qo'yish
    answers = [correct_answer] + wrong_answers
    random.shuffle(answers)
    correct_index = answers.index(correct_answer)
    
    return {
        "id": question_num,
        "question": f"❓ Savol {question_num + 1}/10 (O'rta)\n\n{question_text} = ?",
        "answers": [str(ans) for ans in answers],
        "correct": correct_index
    }


def generate_hard_question(question_num: int) -> dict:
    """Qiyin savol yaratish (darajalar, tenglamalar, murakkab amallar)"""
    question_type = random.choice(['power', 'equation', 'complex'])
    
    if question_type == 'power':
        # Darajalar: a^b + c^d
        base1 = random.randint(2, 5)
        exp1 = random.randint(2, 3)
        base2 = random.randint(2, 5)
        exp2 = random.randint(2, 3)
        correct_answer = (base1 ** exp1) + (base2 ** exp2)
        question_text = f"{base1}^{exp1} + {base2}^{exp2}"
        
    elif question_type == 'equation':
        # Tenglama: x + a = b
        a = random.randint(10, 30)
        b = random.randint(40, 80)
        correct_answer = b - a
        question_text = f"Agar x + {a} = {b} bo'lsa, x = ?"
        
    else:  # complex
        # Murakkab amal: (a + b) × c - d
        a = random.randint(5, 20)
        b = random.randint(5, 20)
        c = random.randint(2, 5)
        d = random.randint(5, 15)
        correct_answer = (a + b) * c - d
        question_text = f"({a} + {b}) × {c} - {d}"
    
    # Noto'g'ri javoblar yaratish
    wrong_answers = []
    while len(wrong_answers) < 3:
        offset = random.randint(-10, 10)
        if offset == 0:
            continue
        wrong = correct_answer + offset
        if wrong > 0 and wrong not in wrong_answers and wrong != correct_answer:
            wrong_answers.append(wrong)
    
    # Javoblarni aralashtirib qo'yish
    answers = [correct_answer] + wrong_answers
    random.shuffle(answers)
    correct_index = answers.index(correct_answer)
    
    return {
        "id": question_num,
        "question": f"❓ Savol {question_num + 1}/10 (Qiyin)\n\n{question_text} = ?",
        "answers": [str(ans) for ans in answers],
        "correct": correct_index
    }


def generate_test_questions() -> List[dict]:
    """10 ta tasodifiy savol yaratish (3 oson, 4 o'rta, 3 qiyin)"""
    questions = []
    
    # 3 ta oson savol
    for i in range(3):
        questions.append(generate_easy_question(i))
    
    # 4 ta o'rta savol
    for i in range(3, 7):
        questions.append(generate_medium_question(i))
    
    # 3 ta qiyin savol
    for i in range(7, 10):
        questions.append(generate_hard_question(i))
    
    return questions


# ============================================================================
# FOYDALANUVCHILAR MA'LUMOTLARI OMBORI
# ============================================================================

# Foydalanuvchilar progressini saqlash uchun lug'at
# Struktura: {user_id: {"current_question": int, "correct_answers": int, "questions": list}}
user_sessions: Dict[int, dict] = {}


# ============================================================================
# KLAVIATURALAR
# ============================================================================

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """3 ta tugma bilan asosiy Reply klaviaturasini yaratish"""
    keyboard = [
        [KeyboardButton(text="📝 Testni boshlash")],
        [KeyboardButton(text="❓ Yordam")],
        [KeyboardButton(text="👤 Muallif haqida")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Harakatni tanlang..."
    )


def get_question_keyboard(question: dict, question_id: int) -> InlineKeyboardMarkup:
    """Savol uchun javob variantlari bilan Inline klaviaturasini yaratish"""
    buttons = []
    
    for idx, answer in enumerate(question["answers"]):
        is_correct = (idx == question["correct"])
        callback_data = QuestionCallback(
            question_id=question_id,
            answer_id=idx,
            is_correct=is_correct
        )
        buttons.append([
            InlineKeyboardButton(
                text=answer,
                callback_data=callback_data.pack()
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ============================================================================
# BUYRUQLAR ISHLOVCHILARI
# ============================================================================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Buyruq /start ishlovchisi - salomlashish va asosiy menyuni ko'rsatish"""
    user = message.from_user
    logger.info(f"📌 /start buyrug'i - Foydalanuvchi: {user.full_name} (ID: {user.id})")
    
    welcome_text = (
        "👋 <b>Matematika Testiga xush kelibsiz!</b>\n\n"
        "Men sizning matematika bilimingizni tekshirishga yordam beraman.\n"
        "Test turli qiyinlikdagi 10 ta savoldan iborat:\n"
        "• Oson (qo'shish, ayirish)\n"
        "• O'rta (ko'paytirish, bo'lish)\n"
        "• Qiyin (darajalar, tenglamalar, mantiq)\n\n"
        "Quyidagi tugmalar yordamida harakatni tanlang 👇"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )


@dp.message(Command("test"))
async def cmd_test(message: Message):
    """Buyruq /test ishlovchisi - testni boshlash"""
    user = message.from_user
    logger.info(f"📌 /test buyrug'i - Foydalanuvchi: {user.full_name} (ID: {user.id})")
    await start_test(message)


# ============================================================================
# REPLY TUGMALAR ISHLOVCHILARI
# ============================================================================

@dp.message(F.text == "📝 Testni boshlash")
async def button_start_test(message: Message):
    """'Testni boshlash' tugmasi ishlovchisi"""
    user = message.from_user
    logger.info(f"🔘 '📝 Testni boshlash' tugmasi bosildi - Foydalanuvchi: {user.full_name} (ID: {user.id})")
    await start_test(message)


@dp.message(F.text == "❓ Yordam")
async def button_help(message: Message):
    """'Yordam' tugmasi ishlovchisi"""
    user = message.from_user
    logger.info(f"🔘 '❓ Yordam' tugmasi bosildi - Foydalanuvchi: {user.full_name} (ID: {user.id})")
    
    help_text = (
        "📚 <b>Botdan foydalanish bo'yicha ko'rsatma</b>\n\n"
        "<b>Testni qanday topshirish:</b>\n"
        "1️⃣ '📝 Testni boshlash' tugmasini bosing yoki /test buyrug'ini yuboring\n"
        "2️⃣ Sizga 10 ta savol beriladi\n"
        "3️⃣ Har bir savol uchun 4 ta javob variantidan birini tanlang\n"
        "4️⃣ Javob tanlaganingizdan keyin to'g'ri yoki noto'g'ri ekanligini ko'rasiz\n"
        "5️⃣ 10-savoldan keyin umumiy natijangizni olasiz\n\n"
        "<b>Qiyinlik darajalari:</b>\n"
        "🟢 Oson - oddiy arifmetik amallar\n"
        "🟡 O'rta - ko'paytirish va bo'lish\n"
        "🔴 Qiyin - darajalar, tenglamalar, mantiqiy masalalar\n\n"
        "Omad! 🍀"
    )
    
    await message.answer(help_text, parse_mode="HTML")


@dp.message(F.text == "👤 Muallif haqida")
async def button_about(message: Message):
    """'Muallif haqida' tugmasi ishlovchisi"""
    user = message.from_user
    logger.info(f"🔘 '👤 Muallif haqida' tugmasi bosildi - Foydalanuvchi: {user.full_name} (ID: {user.id})")
    
    about_text = (
        "👨‍💻 <b>Bot yaratuvchisi haqida</b>\n\n"
        "Ushbu bot matematikani o'rganishga yordam berish "
        "va bilimlarni o'yin shaklida tekshirish uchun yaratilgan.\n\n"
        "<b>Texnologiyalar:</b>\n"
        "• Python 3.x\n"
        "• aiogram 3.24 (Telegram Bot Framework)\n"
        "• Asinxron dasturlash\n\n"
        "<b>Imkoniyatlar:</b>\n"
        "✅ Har safar yangi 10 ta savol\n"
        "✅ Turli qiyinlikdagi savollar\n"
        "✅ Tezkor javob qaytarish\n"
        "✅ Natijalarni hisoblash\n"
        "✅ Qulay interfeys\n\n"
        "Versiya: 2.0\n"
        "Yil: 2026"
    )
    
    await message.answer(about_text, parse_mode="HTML")


# ============================================================================
# TEST LOGIKASI
# ============================================================================

async def start_test(message: Message):
    """Foydalanuvchi uchun yangi testni boshlash"""
    user_id = message.from_user.id
    user = message.from_user
    
    logger.info(f"🎯 Test boshlandi - Foydalanuvchi: {user.full_name} (ID: {user.id})")
    
    # Yangi savollar to'plamini yaratish
    questions = generate_test_questions()
    
    # Foydalanuvchi sessiyasini boshlash
    user_sessions[user_id] = {
        "current_question": 0,
        "correct_answers": 0,
        "questions": questions
    }
    
    start_text = (
        "🎯 <b>Test boshlandi!</b>\n\n"
        "Sizga 10 ta savol beriladi.\n"
        "Taklif etilgan variantlardan to'g'ri javobni tanlang.\n\n"
        "Omad! 🚀"
    )
    
    await message.answer(start_text, parse_mode="HTML")
    
    # Birinchi savolni yuborish
    await send_question(message.from_user.id, 0)


async def send_question(user_id: int, question_id: int):
    """Foydalanuvchiga savolni yuborish"""
    session = user_sessions[user_id]
    question = session["questions"][question_id]
    keyboard = get_question_keyboard(question, question_id)
    
    await bot.send_message(
        chat_id=user_id,
        text=question["question"],
        reply_markup=keyboard
    )


# ============================================================================
# CALLBACK SO'ROVLAR (SAVOLLARGA JAVOBLAR)
# ============================================================================

@dp.callback_query(QuestionCallback.filter())
async def process_answer(callback: CallbackQuery, callback_data: QuestionCallback):
    """Savollarga javoblar ishlovchisi"""
    user_id = callback.from_user.id
    user = callback.from_user
    
    # Faol sessiya borligini tekshirish
    if user_id not in user_sessions:
        await callback.answer(
            "❌ Sessiya tugadi. Testni qaytadan boshlang!",
            show_alert=False
        )
        return
    
    session = user_sessions[user_id]
    
    # Foydalanuvchi joriy savolga javob berayotganini tekshirish
    if callback_data.question_id != session["current_question"]:
        await callback.answer(
            "⚠️ Bu savol allaqachon o'tkazilgan!",
            show_alert=False
        )
        return
    
    # To'g'ri javoblar hisoblagichini yangilash
    current_question = session["questions"][callback_data.question_id]
    if callback_data.is_correct:
        session["correct_answers"] += 1
        alert_text = "✅ To'g'ri! Ajoyib!"
        logger.info(f"✅ To'g'ri javob - Savol {callback_data.question_id + 1}/10 - Foydalanuvchi: {user.full_name} (ID: {user.id})")
    else:
        correct_answer = current_question["answers"][current_question["correct"]]
        alert_text = f"❌ Noto'g'ri!\nTo'g'ri javob: {correct_answer}"
        logger.info(f"❌ Noto'g'ri javob - Savol {callback_data.question_id + 1}/10 - Foydalanuvchi: {user.full_name} (ID: {user.id})")
    
    # Pop-up xabarni ko'rsatish
    await callback.answer(alert_text, show_alert=False)
    
    # Keyingi savolga o'tish
    session["current_question"] += 1
    
    # Yana savollar borligini tekshirish
    if session["current_question"] < 10:
        # Keyingi savolni yuborish
        await send_question(user_id, session["current_question"])
    else:
        # Test tugadi - natijalarni ko'rsatish
        await show_results(user_id)


async def show_results(user_id: int):
    """Test natijalarini ko'rsatish"""
    session = user_sessions[user_id]
    correct = session["correct_answers"]
    total = 10
    percentage = (correct / total) * 100
    
    # Natijaga qarab xabarni aniqlash
    if percentage == 100:
        emoji = "🏆"
        message = "Ajoyib! Barcha savollarga to'g'ri javob berdingiz!"
        recommendation = "Siz - matematika dahosi! 🌟"
    elif percentage >= 80:
        emoji = "🎉"
        message = "A'lo! Juda yaxshi natija!"
        recommendation = "Shunday davom eting! 💪"
    elif percentage >= 60:
        emoji = "👍"
        message = "Yaxshi! Yomon emas!"
        recommendation = "Yana bir oz mashq qiling va mukammal bo'ladi! 📚"
    elif percentage >= 40:
        emoji = "📖"
        message = "Yomon emas!"
        recommendation = "Materialni takrorlashni va qayta urinib ko'rishni tavsiya qilaman! 🎯"
    else:
        emoji = "💪"
        message = "Xafa bo'lmang!"
        recommendation = "Mashq sizni kuchli qiladi! Yana urinib ko'ring! 🚀"
    
    results_text = (
        f"{emoji} <b>Test tugadi!</b>\n\n"
        f"📊 <b>Sizning natijangiz:</b>\n"
        f"To'g'ri javoblar: {correct} / {total}\n"
        f"Foiz: {percentage:.1f}%\n\n"
        f"💬 {message}\n"
        f"{recommendation}\n\n"
        f"Yana urinib ko'rmoqchimisiz? '📝 Testni boshlash' tugmasini bosing!"
    )
    
    await bot.send_message(
        chat_id=user_id,
        text=results_text,
        parse_mode="HTML"
    )
    
    # Natijalarni logga yozish
    user_info = await bot.get_chat(user_id)
    logger.info(f"🏁 Test tugadi - Natija: {correct}/10 ({percentage:.1f}%) - Foydalanuvchi: {user_info.full_name} (ID: {user_id})")
    
    # Foydalanuvchi sessiyasini o'chirish
    del user_sessions[user_id]


# ============================================================================
# BOTNI ISHGA TUSHIRISH
# ============================================================================

async def main():
    """Botni ishga tushirish uchun asosiy funksiya"""
    logger.info("Bot ishga tushmoqda...")
    
    # Webhooklarni o'chirish (agar bo'lsa)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Pollingni boshlash
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot foydalanuvchi tomonidan to'xtatildi")
