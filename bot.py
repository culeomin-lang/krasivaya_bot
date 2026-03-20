import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN", "8699201233:AAFg0xXHxxYuaXOrIVxvxEQKsMikx0T5oZ0")

PDF_LINKS = {
    "golden_ring": "https://drive.google.com/your_link_1",
    "karelia": "https://drive.google.com/your_link_2",
    "sochi": "https://drive.google.com/your_link_3"
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Золотое кольцо", callback_data="golden_ring")],
        [InlineKeyboardButton("Карелия (Кижи, Валаам)", callback_data="karelia")],
        [InlineKeyboardButton("Сочи и Адлер", callback_data="sochi")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я помогу получить подробный маршрут для автотуристов.\n\nВыбери маршрут:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    route = query.data
    prices = [{"label": "Маршрут", "amount": 50}]
    
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title="Маршрут для автотуриста",
        description="Подробный маршрут с отелями, кафе и советами",
        payload=route,
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="route_payment"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.successful_payment:
        route = update.message.successful_payment.invoice_payload
        pdf_url = PDF_LINKS.get(route)
        await update.message.reply_text(
            f"Спасибо за покупку!\n\nСсылка на маршрут: {pdf_url}\n\nСохрани её — она не потеряется."
        )
    elif update.message.pre_checkout_query:
        await update.message.pre_checkout_query.answer(ok=True)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    
    print("Бот запущен")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
