from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = ""

questions = [
    {
        "question": "1-savol: Python’da list yaratish uchun qaysi belgidan foydalanamiz?",
        "options": ["()", "[]", "{}"],
        "answer": "[]"
    },
    {
        "question": "2-savol: Django nima?",
        "options": ["Framework", "Kutubxona", "Ma'lumotlar bazasi"],
        "answer": "Framework"
    },
    {
        "question": "3-savol: GitHub nima uchun ishlatiladi?",
        "options": ["Versiya nazorati", "To'lov tizimi", "Messendjer"],
        "answer": "Versiya nazorati"
    },
]

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"score": 0, "q_index": 0}
    await send_question(update, context, user_id)


async def send_question(update_or_id, context, user_id):
    data = user_data[user_id]
    q_index = data["q_index"]

    if q_index < len(questions):
        q = questions[q_index]
        buttons = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in q["options"]]
        reply_markup = InlineKeyboardMarkup(buttons)

        if isinstance(update_or_id, Update):
            await update_or_id.message.reply_text(q["question"], reply_markup=reply_markup)
        else:
            await context.bot.send_message(user_id, q["question"], reply_markup=reply_markup)
    else:
        score = data["score"]
        await context.bot.send_message(user_id, f"✅ Test tugadi!\nNatijangiz: {score}/{len(questions)} ball")


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = user_data[user_id]
    q_index = data["q_index"]
    q = questions[q_index]

    if query.data == q["answer"]:
        data["score"] += 1
        await query.edit_message_text(f"{q['question']}\n\n✅ To‘g‘ri!")
    else:
        await query.edit_message_text(f"{q['question']}\n\n❌ Noto‘g‘ri!")

    data["q_index"] += 1
    await send_question(user_id, context, user_id)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(answer))

    print("🤖 Bot ishlamoqda...")
    app.run_polling()


if __name__ == "__main__":
    main()
