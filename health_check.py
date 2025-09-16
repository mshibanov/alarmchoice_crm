# health_check.py (новый файл для проверки здоровья)
from aiohttp import web

async def health_check(request):
    return web.Response(text="OK", status=200)

app = web.Application()
app.router.add_get('/health', health_check)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)