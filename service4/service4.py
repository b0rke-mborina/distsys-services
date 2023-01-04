import pathlib
import aiofiles
from aiohttp import web

receivedCode = []

routes = web.RouteTableDef()

@routes.post("/gatherData")
async def function(request):
	global receivedCode
	try:
		# store received code to storage list
		data = await request.json()
		receivedCode.append({"username": data.get("username"), "content": data.get("content")})

		# save stored code / content to files
		if len(receivedCode) > 10:
			pathlib.Path("files").mkdir(parents = True, exist_ok = True)
			for item in receivedCode:
				async with aiofiles.open("files/%s.txt"%(item.get("username")), "w") as writer:
					await writer.write(item.get("content"))
			receivedCode.clear()

		return web.json_response({"name": "service4", "status": "OK"}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service4", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8084)
