import aiohttp
import asyncio
from aiohttp import web
from helperFunctions import forwardToWorkerTokenizer, fetchRepositoryCode

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			# get data from service 0
			task = asyncio.create_task(session.get("http://service0:8080/"))
			response = await asyncio.gather(task)
			responseData = await response[0].json()

			# save data to desired format
			dictionaryData = [
				{"id": item[0], "username": item[1], "ghlink": item[2], "filename": item[3], "content": item[4]} for item in responseData.get("data")
			]
			"""dictionaryData = [
				{"id": item[0], "username": item[1], "ghlink": item[2], "filename": item[3], "content": await fetchRepositoryCode(item[2], item[3])} for item in responseData.get("data")
			]"""

			# forward data to worker tokenizers in dictinary format
			service2Response = await forwardToWorkerTokenizer("http://service2:8082/", dictionaryData)
			service3Response = await forwardToWorkerTokenizer("http://service3:8083/", dictionaryData)

			return web.json_response({"name": "service1", "status": "OK", "response": [service2Response, service3Response]}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service1", "error" : str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8081)
