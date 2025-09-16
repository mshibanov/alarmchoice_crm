# main.py
import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PORT
from alarms_data import find_matching_alarms
from crm_integration import create_crm_deal

# States
AUTOSTART, GSM, GPS, PHONE = range(4)

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"👋🏻 Привет, {user.first_name}!\n\n"
        "Я помогу тебе выбрать сигнализацию на твой автомобиль!\n\n"
        "⁉️ Давай решим, что она должна уметь"
    )

    await ask_autostart(update, context)
    return AUTOSTART


async def ask_autostart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [['😉 С Автозапуском', '🥶 БЕЗ Автозапуска']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "1️⃣ Нужен ли тебе автозапуск?\n\n"
        "❄️ В условиях нашего климата необходимо прогревать двигатель перед поездкой. "
        "Даже если на улице несильный мороз! Это снижает износ двигателя.\n\n"
        "В конце концов просто приятно сесть в прогретый автомобиль 😌\n\n"
        "❓Какую систему выберешь?",
        reply_markup=reply_markup
    )


async def handle_autostart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        choice = update.message.text
        context.user_data['autostart'] = 'С Автозапуском' in choice

        await ask_gsm(update, context)
        return GSM
    except Exception as e:
        logger.error(f"Error in handle_autostart: {e}")
        await update.message.reply_text("Произошла ошибка. Давайте начнем заново /start")
        return ConversationHandler.END


async def ask_gsm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [['😎 Приложение в телефоне', '📵 Брелок']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "2️⃣ Как планируешь управлять системой? Брелок или GSM-модуль\n\n"
        "Можно управлять через брелок, но проблема в том, что сигнал тревоги от автомобиля до брелка "
        "не всегда стабилен и есть шанс не получить сигнал тревоги ⛔️\n\n"
        "Через приложение в телефоне в независимости от вашего местоположения вы получите сообщение "
        "в случае тревоги и сможете отправить команду на автозапуск 👏\n\n"
        "Что выберете❓",
        reply_markup=reply_markup
    )


async def handle_gsm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        choice = update.message.text
        context.user_data['gsm'] = 'Приложение' in choice

        await ask_gps(update, context)
        return GPS
    except Exception as e:
        logger.error(f"Error in handle_gsm: {e}")
        await update.message.reply_text("Произошла ошибка. Давайте начнем заново /start")
        return ConversationHandler.END


async def ask_gps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [['🕵🏻‍♂️ С GPS-антенной', '🙈 БЕЗ GPS-антенны']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Отлично, остался последний вопрос! 3️⃣ GPS-антенна\n\n"
        "🗺 Если вы часто даете машину чужим людям и вам важно отслеживать "
        "точное местоположение автомобиля, то вам необходимо выбрать систему с GPS.\n\n"
        "Ваш вариант❓",
        reply_markup=reply_markup
    )


async def handle_gps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        choice = update.message.text
        context.user_data['gps'] = 'С GPS-антенной' in choice

        # Поиск подходящих сигнализаций
        alarms = find_matching_alarms(
            context.user_data['autostart'],
            context.user_data['gsm'],
            context.user_data['gps']
        )

        await show_recommendations(update, context, alarms)
        return PHONE
    except Exception as e:
        logger.error(f"Error in handle_gps: {e}")
        await update.message.reply_text("Произошла ошибка. Давайте начнем заново /start")
        return ConversationHandler.END


async def show_recommendations(update: Update, context: ContextTypes.DEFAULT_TYPE, alarms: list) -> None:
    try:
        user_data = context.user_data

        message = (
            f"🔍 Для вас важно, чтобы сигнализация имела следующий функционал:\n\n"
            f"• {'✅' if user_data['autostart'] else '❌'} {'С' if user_data['autostart'] else 'БЕЗ'} автозапуска\n"
            f"• {'📱' if user_data['gsm'] else '📟'} Управление через {'приложение' if user_data['gsm'] else 'брелок'}\n"
            f"• {'✅' if user_data['gps'] else '❌'} {'С' if user_data['gps'] else 'БЕЗ'} GPS-отслеживания\n\n"
        )

        if alarms:
            message += f"Нашлось {len(alarms)} подходящих систем:\n\n"

            for alarm in alarms:
                features = []
                if alarm['autostart']: features.append("автозапуск")
                if alarm['remote']: features.append("брелок")
                if alarm['gsm']: features.append("приложение")
                if alarm['gps']: features.append("GPS")

                message += (
                    f"🐼 {alarm['name']}\n"
                    f"• Характеристики: {', '.join(features)}\n"
                    f"• Стоимость: {alarm['price']}\n"
                    f"• Ссылка: {alarm['link']}\n\n"
                )
        else:
            message += "К сожалению, подходящих систем не найдено 😢\n"

        await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

        # Сохраняем рекомендованные сигнализации
        context.user_data['recommended_alarms'] = alarms

        # Запрос телефона с кнопкой
        keyboard = [[KeyboardButton("📞 Отправить номер телефона", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        await update.message.reply_text(
            "Хочешь узнать стоимость установки на твой авто?💰\n\n"
            "Оставь номер телефона и наш мастер свяжется с тобой и ответит на все вопросы📞\n\n"
            "Мы официальные представители Pandora и StarLine в Самаре 👨🏻‍🔧\n\n"
            "Нажми кнопку ниже, чтобы поделиться номером телефона 👇",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in show_recommendations: {e}")
        await update.message.reply_text("Произошла ошибка при показе рекомендаций. Давайте начнем заново /start")


async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        if update.message.contact:
            phone = update.message.contact.phone_number
        else:
            phone = update.message.text

        context.user_data['phone'] = phone
        context.user_data['username'] = update.message.from_user.first_name

        # Создаем сделку в CRM
        success = create_crm_deal(
            context.user_data,
            context.user_data.get('recommended_alarms', [])
        )

        # Клавиатура для повторного опроса
        keyboard = [['🔄 Пройти опрос еще раз']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        if success:
            await update.message.reply_text(
                "✅ Спасибо! Ваша заявка принята!\n"
                "Наш мастер свяжется с вами в ближайшее время для консультации 📞\n\n"
                "Хочешь подобрать другую сигнализацию?",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "✅ Спасибо за ваши ответы!\n"
                "К сожалению, сейчас не можем обработать заявку. "
                "Пожалуйста, позвоните нам напрямую 📞\n\n"
                "Хочешь подобрать другую сигнализацию?",
                reply_markup=reply_markup
            )

        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in handle_phone: {e}")
        await update.message.reply_text("Произошла ошибка при обработке номера телефона. Давайте начнем заново /start")
        return ConversationHandler.END


async def handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для повторного прохождения опроса"""
    try:
        if update.message.text == '🔄 Пройти опрос еще раз':
            await start(update, context)
    except Exception as e:
        logger.error(f"Error in handle_restart: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуйте еще раз /start")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Диалог отменен', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)


async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка здоровья бота"""
    await update.message.reply_text("Бот работает нормально! ✅")


def setup_application():
    """Настройка и создание приложения"""
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаем обработчик диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AUTOSTART: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_autostart)],
            GSM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gsm)],
            GPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gps)],
            PHONE: [MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), handle_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_restart))
    application.add_handler(CommandHandler('health', health_check))
    application.add_error_handler(error_handler)

    return application


def main():
    """Основная функция"""
    # Проверяем, запущен ли в Amvera (есть ли переменная окружения)
    is_amvera = os.getenv('AMVERA_APP_NAME') is not None

    application = setup_application()

    if is_amvera:
        # Запуск в Amvera с вебхуками
        logger.info("Запуск в режиме вебхука для Amvera")
        application.run_webhook(
            listen="0.0.0.0",
            port=WEBHOOK_PORT,
            webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
            secret_token='WEBHOOK_SECRET_TOKEN'
        )
    else:
        # Локальная разработка с polling
        logger.info("Запуск в режиме polling для локальной разработки")
        application.run_polling()


if __name__ == '__main__':
    main()