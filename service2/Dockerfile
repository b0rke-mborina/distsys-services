FROM python:3.9.13

RUN pip install aiohttp

COPY service2.py ./
COPY helperFunctions.py ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "./service2.py"]
