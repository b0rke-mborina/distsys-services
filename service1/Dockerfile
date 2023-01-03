FROM python:3.9.13

# WORKDIR ./

RUN pip install aiosqlite aiohttp asyncio numpy pandas

COPY service1.py ./
COPY helperFunctions.py ./

CMD ["python", "./service1.py"]

# CMD ["curl", "http://127.0.0.1:8081/"]
