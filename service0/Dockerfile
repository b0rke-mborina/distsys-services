FROM python:3.9.13

RUN pip install asyncio aiosqlite aiohttp numpy pandas

COPY service0.py ./
COPY helperFunctions.py ./
COPY distsys-services-database.db ./
COPY data/dataset.json ./data/

CMD ["python", "./service0.py"]
