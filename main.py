import os
from telegram import Update, ForceReply, LabeledPrice
from telegram.ext import Application, CommandHandler, MessageHandler, PreCheckoutQueryHandler, filters, CallbackContext
from dotenv import load_dotenv
import openai

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN =str(os.getenv("TELEGRAM_TOKEN"))
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")


# Инициализация клиента OpenAI
openai.api_key = OPENAI_TOKEN
client = openai.OpenAI(api_key=OPENAI_TOKEN)

# Глобальный словарь для подсчета сообщений пользователей
user_message_count = {}



async def  start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение и помощь по командам."""
    if update.message:
        await update.message.reply_text("Привет! Напиши мне что-нибудь, и я отвечу. \nПервые 30 сообщений бесплатно, далее по подписке, 350 руб в месяц.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handles incoming messages and replies through GPT."""

    user_id = update.effective_user.id

    # Initialize message count for new users
    if user_id not in user_message_count:
        user_message_count[user_id] = 0

    # Increment user message count
    user_message_count[user_id] += 1

    # Apply limit only for non-subscribers
    if  user_message_count[user_id] > 30:
        if update.message:
            await update.message.reply_text(
                "Вы превысили лимит бесплатных сообщений. Пожалуйста, подпишитесь для продолжения."
            )
        return

    # If subscription is fine or under limit, continue with message handling
    prompt = update.message.text if update.message else ""

    try:
        # Send prompt to GPT-4 or relevant model
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Correct model name
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )

        # Extract response text
        reply_text = response.choices[0]['message']['content']

        # Send response back to user
        if update.message:
            await update.message.reply_text(reply_text)
    except Exception as e:
        # Handle any errors from the API or communication
        await update.message.reply_text("Произошла ошибка при запросе к GPT. Попробуйте еще раз.")
        print(f"Error handling GPT response: {e}")


def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print('yes')
    app.run_polling()

if __name__ == '__main__':
    main()
