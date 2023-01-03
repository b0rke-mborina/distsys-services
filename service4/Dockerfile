FROM python:3.9.13

# WORKDIR ./

RUN pip install aiohttp aiofiles pathlib

COPY service4.py ./

CMD ["python", "./service4.py"]

# docker run -d -p 8084:8084 distsys-service4