from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot_commands import start, handle_message
from db_handler import init_db

def main():
    """Запуск Telegram-бота."""
    TOKEN = '7744936512:AAHc-A50a3HJYbbJK6M1WsMfs5_nXa2suCo'

    init_db()

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()