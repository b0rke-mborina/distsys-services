FROM python:3.9.13

# WORKDIR ./

RUN pip install aiosqlite aiohttp numpy pandas

COPY service2.py ./
COPY helperFunctions.py ./

CMD ["python", "./service2.py"]
