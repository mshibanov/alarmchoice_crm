import asyncio
from aiohttp import web
from main import setup_application
from config import WEBHOOK_PATH, BOT_TOKEN


async def handle_webhook(request):
    """Обработчик вебхуков"""
    application = request.app['application']

    # Проверяем, что запрос содержит JSON
    if request.content_type != 'application/json':
        return web.Response(status=400, text="Invalid content type")

    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return web.Response(status=200, text="OK")
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return web.Response(status=500, text="Internal server error")


async def init_app():
    """Инициализация приложения"""
    application = setup_application()

    # Создаем aiohttp приложение
    app = web.Application()
    app['application'] = application

    # Добавляем маршрут для вебхука
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # Добавляем health check endpoint
    async def health_check(request):
        return web.Response(text="Bot is running")

    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)

    return app


if __name__ == '__main__':
    # Запуск для локального тестирования
    web.run_app(init_app(), port=8080)