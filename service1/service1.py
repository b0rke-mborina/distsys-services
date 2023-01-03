import aiohttp
import asyncio
from aiohttp import web
from helperFunctions import forwardToWorkerTokenizer

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			task = asyncio.create_task(session.get("http://service0:8080/"))
			response = await asyncio.gather(task)
			responseData = await response[0].json()
			# print(responseData.get("data")[0])
			# print(responseData.get("data")[0][1])
			# print(len(responseData.get("data")))

			# forward data to worker tokenizers in dictinary format
			dictionaryData = [
				{"id": item[0], "username": item[1], "ghlink": item[2], "filename": item[3], "content": item[4]} for item in responseData.get("data")
			]
			# print(dictionaryData)
			service2Response = await forwardToWorkerTokenizer("http://service2:8082/", dictionaryData)
			service3Response = await forwardToWorkerTokenizer("http://service3:8083/", dictionaryData)

			return web.json_response({"name": "service1", "status": "OK", "response": [service2Response, service3Response]}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service1", "error" : str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8081)
