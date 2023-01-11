FROM python:3.9.13

RUN pip install aiohttp aiofiles pathlib

COPY service4.py ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "./service4.py"]
