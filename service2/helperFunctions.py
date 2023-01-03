import aiohttp


# forwards request to service4
async def forwardToService4(data):
	async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
		async with session.post("http://service4:8084/gatherData", json = data) as response:
			service4Response = await response.json()
	return service4Response
