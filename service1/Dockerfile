FROM python:3.9.13

RUN pip install aiohttp asyncio

COPY service1.py ./
COPY helperFunctions.py ./

CMD ["python", "./service1.py"]
