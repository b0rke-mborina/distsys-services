# distsys-services

**To start all services use command (in project root folder):**
- docker compose up

**Send GET request to:**
- *http://localhost:8081/* (default functionality)
- *http://localhost:8080/* (adding data to database and retrieving random data from database)

**To build one service use command (in desired service folder):**
- docker build -t distsys-service0 .
- docker build -t distsys-service1 .
- docker build -t distsys-service2 .
- docker build -t distsys-service3 .
- docker build -t distsys-service4 .

**To start one service use command (in desired service folder):**
- docker run -d -p 8084:8084 distsys-service0
- docker run -d -p 8084:8084 distsys-service1
- docker run -d -p 8084:8084 distsys-service2
- docker run -d -p 8084:8084 distsys-service3
- docker run -d -p 8084:8084 distsys-service4

**Commented out features / functionalities:**
- returning only links and usernames (service0)
- adding data to database before start (service0)
- cloning repository code and getting code from file (service1)
- adding data to blockchain (service0)
- getting data from blockchain (service0)

**To test all services use command (in project root folder, while all services are running):**
- python -m pytest -v

**Data in *service0/data/dataset.json*:**  https://huggingface.co/datasets/codeparrot/codeparrot-clean/resolve/main/file-000000000040.json.gz

**Dependencies:**
- aiosqlite
- aiohttp
- asyncio
- aiofiles
- pathlib
- numpy
- pandas
- pytest
- gitpython
- python-dotenv
- web3
- vyper
