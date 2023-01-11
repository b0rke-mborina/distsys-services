FROM python:3.9.13

RUN pip install asyncio aiosqlite aiohttp numpy pandas python-dotenv web3

COPY service0.py ./
COPY helperFunctions.py ./
COPY distsys-services-database.db ./
COPY data/dataset.json ./data/
COPY web3Vyper.py ./
COPY abi.json ./
COPY .env ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "./service0.py"]
