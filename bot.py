# bot.py
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import config
from generators import (
    generate_name_address,
    generate_credit_card,
    generate_boundary_strings,
    generate_temp_email
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Клавиатура с основными кнопками 
MAIN_KEYBOARD = [
    ["🇷🇺 ФИО и адрес (RU)", "🇺🇸 ФИО и адрес (EN)"],
    ["💳 Номер карты", "📏 Граничные строки"],
    ["📧 Временный email", "🆘 Помощь"]
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приветственное сообщение и показывает клавиатуру."""
    welcome_text = (
        "🛠️ *Test Data Factory Bot*\n\n"
        "Я помогаю создавать тестовые данные для проверки ПО.\n"
        "Выберите тип данных на клавиатуре ниже:\n\n"
        "• *ФИО и адрес* — реалистичные данные на русском и английском\n"
        "• *Номер карты* — валидный номер (алгоритм Луна)\n"
        "• *Граничные строки* — для проверки полей ввода и безопасности\n"
        "• *Временный email* — адрес для одноразовой почты\n\n"
        "Также используйте команды:\n"
        "/start - перезапуск бота\n"
        "/help - справка"
    )
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

# Команда /help 
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает справку по использованию бота."""
    help_text = (
        "📚 *Справка по Test Data Factory*\n\n"
        "*Как использовать:*\n"
        "1. Просто нажмите на одну из кнопок клавиатуры.\n"
        "2. Бот мгновенно сгенерирует данные.\n\n"
        "*Описание генераторов:*\n"
        "• *ФИО и адрес* — реалистичные персональные данные на русском и английском.\n"
        "• *Номер карты* — генерируется по алгоритму Луна. Это *НЕ настоящая* карта!\n"
        "• *Граничные строки* — данные для тестирования полей ввода (ограничения, инъекции, спецсимволы).\n"
        "• *Временный email* — адрес на одноразовых почтовых сервисах.\n\n"
        "⚠️ *Важно:* Все данные сгенерированы случайно и используются только для тестирования."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

# Обработчик кнопок клавиатуры
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатия кнопок клавиатуры."""
    text = update.message.text

    if text == "🇷🇺 ФИО и адрес (RU)":
        data = generate_name_address('ru')
        response = (
            f"*ФИО и адрес (RU):*\n\n"
            f"👤 *ФИО:* {data['full_name']}\n"
            f"🏠 *Адрес:* {data['address']}\n"
            f"📞 *Телефон:* {data['phone']}"
        )

    elif text == "🇺🇸 ФИО и адрес (EN)":
        data = generate_name_address('en')
        response = (
            f"*Name and Address (EN):*\n\n"
            f"👤 *Full Name:* {data['full_name']}\n"
            f"🏠 *Address:* {data['address']}\n"
            f"📞 *Phone:* {data['phone']}"
        )

    elif text == "💳 Номер карты":
        data = generate_credit_card()
        response = (
            f"*Тестовая кредитная карта:*\n\n"
            f"🔢 *Номер:* `{data['number']}`\n"
            f"🏷️ *Тип:* {data['type']}\n"
            f"📅 *Срок:* {data['expiry']}\n"
            f"🔐 *CVV:* {data['cvv']}\n\n"
            f"⚠️ *Это НЕ настоящая карта!* Используйте только для тестов."
        )

    elif text == "📏 Граничные строки":
        strings = generate_boundary_strings()
        response = "*Граничные строки и инъекции:*\n\n"
        
        for item in strings:
            # Форматируем вывод красиво
            response += f"*{item['title']}*\n"
            response += f"_{item['description']}_\n"
            # Для пустой строки показываем специальное сообщение
            if item['value'] == '':
                response += "`[ПУСТАЯ СТРОКА]`\n"
            else:
                # Обрезаем слишком длинные строки для читаемости
                preview = item['value']
                if len(preview) > 100:
                    preview = preview[:100] + "..."
                response += f"```\n{preview}\n```\n"
            response += f"Длина: {len(item['value'])} символов\n\n"
        
        response += "💡 *Совет:* Используйте эти строки для тестирования:\n"
        response += "• Валидации полей ввода\n• Обработки спецсимволов\n• Защиты от инъекций"

    elif text == "📧 Временный email":
        data = generate_temp_email()
        response = (
            f"*Временный email адрес:*\n\n"
            f"📭 `{data['email']}`\n\n"
            f"*Примечание:* {data['note']}"
        )

    elif text == "🆘 Помощь":
        # Вызываем ту же функцию, что и для команды /help
        await help_command(update, context)
        return  # Важно: выходим, чтобы не отправлять дополнительный ответ

    else:
        response = "Пожалуйста, используйте кнопки клавиатуры или команду /help."
        await update.message.reply_text(response, parse_mode='Markdown')
        return

    # Отправляем ответ (кроме случаев, где уже отправили, как с "Помощь")
    await update.message.reply_text(response, parse_mode='Markdown')

# Основная функция
def main():
    """Запуск бота."""
    # Создаем приложение
    application = Application.builder().token(config.BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))  # Регистрируем команду /help

    # Регистрируем обработчик текстовых сообщений (кнопки)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()