from aiohttp import web
from helperFunctions import forwardToService4

responses = []

routes = web.RouteTableDef()

@routes.post("/")
async def function(request):
	global responses
	try:
		responseData = await request.json()
		if responseData.get("username").lower().startswith("d"):
			# print("Found row with username starting with 'd':", responseData.get("username"))
			response = await forwardToService4(responseData)
			# print(response)
			responses.append(response)
		# print(responses)

		return web.json_response({"name": "service3", "status": "OK", "service4 responses": responses}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service3", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8083)