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
		record = await request.json()
		# print("Username:", record.get("username"))
		# print("Content:", record.get("content").split("\n")[0])
		receivedCode.append({"username": record.get("username"), "content": record.get("content")})
		# print("Code", {"username": record.get("username"), "content": record.get("content")}, "received and stored!")
		# print("Storage list", receivedCode)
		# print("Storage list length =", len(receivedCode))

		# save stored code / content to files
		if len(receivedCode) > 10:
			# print("Code / content saving to files initializaed.")
			pathlib.Path("files").mkdir(parents = True, exist_ok = True)
			for item in receivedCode:
				# print(item.get("username"))
				async with aiofiles.open("files/%s.txt"%(item.get("username")), "w") as writer:
					await writer.write(item.get("content"))
			receivedCode.clear()
			# print("Files saved successfuly. List cleaned successfuly.")

		return web.json_response({"name": "service4", "status": "OK"}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service4", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8084)
