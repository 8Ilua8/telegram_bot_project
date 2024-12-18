from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from db_handler import init_db, get_favorites, save_city
from weather_api import get_weather_data

def get_main_menu():
    """Возвращает основное меню кнопок."""
    keyboard = [
        [KeyboardButton("Посмотреть погоду")],
        [KeyboardButton("Добавить в избранное"), KeyboardButton("Показать избранное")],
        [KeyboardButton("О нас")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    await update.message.reply_text(
        "Добро пожаловать! Выберите команду из меню:",
        reply_markup=get_main_menu()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик сообщений пользователя."""
    user_input = update.message.text
    conn, cursor = init_db()

    if user_input == "О нас":
        await update.message.reply_text("Этот бот разработан для получения информации о погоде и сохранения городов в избранное!")

    elif user_input == "Посмотреть погоду":
        await update.message.reply_text("Введите название города:")
        context.user_data["getting_weather"] = True

    elif user_input == "Добавить в избранное":
        await update.message.reply_text("Введите название города, чтобы добавить его в избранное:")
        context.user_data["adding_favorite"] = True

    elif user_input == "Показать избранное":
        favorites = get_favorites(cursor)
        if favorites:
            keyboard = [[KeyboardButton(city)] for city in favorites]
            keyboard.append([KeyboardButton("Назад")])
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Выберите город из избранного:", reply_markup=reply_markup)
            context.user_data["selecting_favorite"] = True
        else:
            await update.message.reply_text("Ваш список избранного пуст.")

    elif context.user_data.get("getting_weather"):
        city = user_input.strip()
        weather_info = get_weather_data(city, cursor, conn)
        if weather_info:
            await update.message.reply_text(weather_info)
        else:
            await update.message.reply_text("Не удалось получить данные о погоде для этого города.")
        context.user_data["getting_weather"] = False

    elif context.user_data.get("adding_favorite"):
        city = user_input.strip()
        save_city(city, cursor, conn)
        await update.message.reply_text(f"Город '{city}' добавлен в избранное!")
        context.user_data["adding_favorite"] = False

    elif context.user_data.get("selecting_favorite"):
        city = user_input.strip()
        if city == "Назад":
            await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=get_main_menu())
            context.user_data["selecting_favorite"] = False
        else:
            favorites = get_favorites(cursor)
            if city in favorites:
                weather_info = get_weather_data(city, cursor, conn)
                if weather_info:
                    await update.message.reply_text(weather_info)
                else:
                    await update.message.reply_text("Не удалось получить данные о погоде для этого города.")
            else:
                await update.message.reply_text("Выбранный город не найден в избранном.")
    else:
        await update.message.reply_text("Пожалуйста, выберите команду из меню.", reply_markup=get_main_menu())

    conn.close()
