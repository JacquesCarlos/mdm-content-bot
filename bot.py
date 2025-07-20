
import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = (
        "Создай контент для флеболога: 1) Текст поста, 2) Идею Reels, 3) Сценарий видео. "
        "ЦА: женщины 30+, симптомы варикоза, тяжесть в ногах. Кратко, экспертно, с CTA."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7,
    )
    message = response.choices[0].message.content
    context.bot_data["last_post"] = message
    await update.message.reply_text(message)

async def post_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = context.bot_data.get("last_post", "Сначала сгенерируй пост с помощью /generate")
    await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
    await update.message.reply_text("✅ Пост отправлен в канал!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("post_now", post_now))
    app.run_polling()
