import aiosqlite
import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	return web.json_response({"name": "service2", "status": "OK"}, status = 200)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8082)
