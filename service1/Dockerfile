FROM python:3.9.13

RUN pip install aiohttp asyncio gitpython aiofiles

COPY service1.py ./
COPY helperFunctions.py ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "./service1.py"]
