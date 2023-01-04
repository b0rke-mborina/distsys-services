import asyncio
import aiohttp
from git import Repo


# used for forwarding data to worker tokenizer (service2 or service3)
async def forwardToWorkerTokenizer(workerTokenizerUrl, data):
	for index in range(len(data)):
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			async with session.post(workerTokenizerUrl, json = data[index]) as response:
				workerTokenizerResponse = await response.json()
	return workerTokenizerResponse

async def fetchRepositoryCode(repository):
	# clone repository which contains file and position in root directory
	eventLoop = asyncio.get_event_loop()
	repositoryContents = await eventLoop.run_in_executor(None, Repo.clone_from, repository, "repository" + repository.split("/")[-1].split(".")[0])
	repositoryTree = repositoryContents.head.commit.tree

	# read all code in the tree's files and return it
	code = ""
	for blob in repositoryTree.traverse():
		if blob.type == "blob":
			code += await eventLoop.run_in_executor(None, blob.data_stream.read)
	return code
