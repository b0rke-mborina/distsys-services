import aiohttp
from aiohttp import web
from helperFunctions import forwardToService4

responses = []

routes = web.RouteTableDef()

@routes.post("/")
async def function(request):
	global responses
	try:
		responseData = await request.json()
		if responseData.get("username").lower().startswith("w"):
			# print("Found row with username starting with 'w':", responseData.get("username"))
			response = await forwardToService4(responseData)
			# print(response)
			responses.append(response)
		# print(responses)
		
		return web.json_response({"name": "service2", "status": "OK", "service4 response": responses}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service3", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8082)
