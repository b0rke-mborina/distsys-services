import asyncio
import aiosqlite
from aiohttp import web
from helperFunctions import fetchRandomRows, addDataToDatabase, addDataToBlockchain, fetchDataFromBlockchain

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		# check if database table is empty
		async with aiosqlite.connect("distsys-services-database.db") as db:
			async with db.execute("SELECT COUNT(1) WHERE EXISTS (SELECT * FROM datatable)") as cursor:
				async for row in cursor:
					# add data to database if database is empty
					if row[0] == 0:
						await addDataToDatabase()
						# await addDataToBlockchain()
					# retrieve random rows
					data = await fetchRandomRows(db)
					# data = await fetchDataFromBlockchain()

		"""usernames = [item[1] for item in data]
		githubLinks = [item[2] for item in data]
		return web.json_response({"service_id": 0, "data": { "usernames": usernames, "githubLinks": githubLinks }}, status = 200)"""
		return web.json_response({"name": "service0", "status": "OK", "data": data}, status = 200)
	except Exception as e:
		return web.json_response({"name": "service0", "error": str(e)}, status = 500)

# fill database with data before start
# asyncio.run(addDataToDatabase())

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8080)
