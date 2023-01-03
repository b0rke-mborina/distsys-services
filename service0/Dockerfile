FROM python:3.9.13

# WORKDIR ./

RUN pip install aiosqlite aiohttp numpy pandas

COPY service0.py ./
COPY helperFunctions.py ./
COPY distsys-services-database.db ./
COPY data/dataset.json ./data/

CMD ["python", "./service0.py"]

# CMD ["curl", "http://127.0.0.1:8081/"]
