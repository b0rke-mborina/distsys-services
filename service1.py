import aiohttp
import asyncio
from aiohttp import web

from helperFunctions import forwardToWorkerTokenizer

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			data = []
			# retrieve random data from service 0
			data.append(asyncio.create_task(session.get("http://127.0.0.1:8080/")))
			response = await asyncio.gather(*data)
			responseData = await response[0].json()
			# print(responseData.get("response")[0])
			# print(responseData.get("response")[0][1])
			# print(len(responseData.get("response")))

			# forward data to worker tokenizers in dictinary format
			dictionaryData = [
				{"id": item[0], "username": item[1], "ghlink": item[2], "filename": item[3], "content": item[4]} for item in responseData.get("response")
			]
			service2Response = await forwardToWorkerTokenizer("http://127.0.0.1:8082/", dictionaryData)
			service3Response = await forwardToWorkerTokenizer("http://127.0.0.1:8083/", dictionaryData)

			return web.json_response({"name": "service1", "status": "OK", "response": [service2Response, service3Response]}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service1", "error" : str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8081)
