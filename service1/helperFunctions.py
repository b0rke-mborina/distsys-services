import asyncio
import aiohttp
import aiofiles
from git import Repo
import os
from os import path

# used for forwarding data to worker tokenizer (service2 or service3)
async def forwardToWorkerTokenizer(workerTokenizerUrl, data):
	for index in range(len(data)):
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			async with session.post(workerTokenizerUrl, json = data[index]) as response:
				workerTokenizerResponse = await response.json()
	return workerTokenizerResponse

async def fetchRepositoryCode(repository, filename):
	try:
		# clone repository to a directory which contains file
		repositoryName = "%s_%s_%s"%("repository", repository.split("/")[-2], repository.split("/")[-1].split(".")[0])
		if not path.exists(repositoryName):
			eventLoop = asyncio.get_event_loop()
			repositoryContents = await eventLoop.run_in_executor(None, Repo.clone_from, repository, repositoryName)

		# get path of file
		relativeFilePath = "./" + filename
		for root, dirs, files in os.walk(repositoryName):  
			if filename in files:
				relativeDirectoryPath = os.path.relpath(root, repositoryName)
				relativeFilePath = repositoryName + "/" + os.path.join(relativeDirectoryPath, filename)

		# read all code in the file async and return it
		code = ""
		async with aiofiles.open(relativeFilePath, mode = 'r') as f:
			async for line in f:
				code += line
		return code
	except Exception as e:
		return "CODE RETRIEVAL FAILED"
