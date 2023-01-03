FROM python:3.9.13

# WORKDIR ./

RUN pip install aiosqlite aiohttp numpy pandas

COPY service3.py ./
COPY helperFunctions.py ./

CMD ["python", "./service3.py"]
