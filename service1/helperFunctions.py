import aiohttp


# used for forwarding data to worker tokenizer (service2 or service3)
async def forwardToWorkerTokenizer(workerTokenizerUrl, data):
	for index in range(len(data)):
		# print("Forwarding data[%s] to WorkerTokenizer"%(index))
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			async with session.post(workerTokenizerUrl, json = data[index]) as response:
				workerTokenizerResponse = await response.json()
	return workerTokenizerResponse
