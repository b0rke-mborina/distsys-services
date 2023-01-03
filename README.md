# distsys-services

To start all services use command (in project root folder):
- docker compose up

To build one service use command (in desired service folder):
- docker build -t distsys-service0 .
- docker build -t distsys-service1 .
- docker build -t distsys-service2 .
- docker build -t distsys-service3 .
- docker build -t distsys-service4 .

To start one service use command (in desired service folder):
- docker run -d -p 8084:8084 distsys-service0
- docker run -d -p 8084:8084 distsys-service1
- docker run -d -p 8084:8084 distsys-service2
- docker run -d -p 8084:8084 distsys-service3
- docker run -d -p 8084:8084 distsys-service4

To test all services use command (in project root folder, while all services are running):
- python -m pytest -v

Dependencies:
- aiosqlite
- aiohttp
- asyncio
- aiofiles
- pathlib
- numpy
- pandas
