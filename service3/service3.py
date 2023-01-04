from aiohttp import web
from helperFunctions import forwardToService4

errorResponses = []

routes = web.RouteTableDef()

@routes.post("/")
async def function(request):
	global errorResponses
	try:
		responseData = await request.json()
		assert isinstance(responseData, dict)
		if responseData.get("username").lower().startswith("d"):
			response = await forwardToService4(responseData)
			if response.get("status") != "OK": errorResponses.append(response)

		return web.json_response({"name": "service3", "status": "OK", "service4 error responses": errorResponses}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service3", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8083)
