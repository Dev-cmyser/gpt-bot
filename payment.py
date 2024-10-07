import os
from telegram import Update, ForceReply, LabeledPrice
from telegram.ext import Application, CommandHandler, MessageHandler, PreCheckoutQueryHandler, filters, CallbackContext

from dotenv import load_dotenv
load_dotenv()

PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Обрабатывает предварительный запрос платежа."""
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        query.answer(ok=True)

def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    """Обработчик успешной оплаты."""
    update.message.reply_text("Спасибо за вашу покупку!")

def payment(update: Update, context: CallbackContext) -> None:
    """Отправляет запрос на оплату."""
    chat_id = update.message.chat_id
    title = "Подписка на использование бота"
    description = "Месячная подписка на использование бота"
    payload = "Custom-Payload"
    currency = "RUB"
    price = 10000  # 100.00 RUB
    prices = [LabeledPrice("Подписка", price)]

    context.bot.send_invoice(chat_id, title, description, payload,
                             PROVIDER_TOKEN, currency, prices)

    # app.add_handler(CommandHandler("pay", payment))
    # app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    # app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
