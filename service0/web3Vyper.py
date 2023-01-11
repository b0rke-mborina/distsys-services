from web3 import Web3
import json
import os
from dotenv import load_dotenv


load_dotenv()

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8090"))
# if not web3.isConnected():
	# print("Connection failed!")

with open("abi.json", "r") as file:
	abi = json.load(file)
address = os.environ["ADDRESS"]
contract = web3.eth.contract(abi = abi, address = address)

def addRecord(username, github_link, filename):
	return contract.functions.addRecord(username, github_link, filename).call()

def getRecord(id):
	return contract.functions.addRecord(id).call()

def getRecordCount():
	return contract.functions.recordCount
