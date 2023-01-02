import pytest
import requests


# tests status codes of all services
class TestStatus:
	def test_service0(self):
		response = requests.get("http://127.0.0.1:8080/")
		assert response.status_code == 200
		pass

	def test_service1(self):
		response = requests.get("http://127.0.0.1:8081/")
		assert response.status_code == 200
		pass

	def test_service2(self):
		requestBody = { "username": "with something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8082/", json = requestBody)
		assert response.status_code == 200
		pass

	def test_service3(self):
		requestBody = { "username": "definately something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8083/", json = requestBody)
		assert response.status_code == 200
		pass

	def test_service4(self):
		requestBody = { "username": "something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8084/gatherData", json = requestBody)
		assert response.status_code == 200
		pass


# tests main properites of all services
class TestReturnProperties:
	def test_service0(self):
		response = requests.get("http://127.0.0.1:8080/")
		data = response.json()
		assert data.get("name") == "service0" and data.get("status") == "OK"
		pass

	def test_service1(self):
		response = requests.get("http://127.0.0.1:8081/")
		data = response.json()
		assert data.get("name") == "service1" and data.get("status") == "OK"
		pass

	def test_service2(self):
		requestBody = { "username": "with something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8082/", json = requestBody)
		data = response.json()
		assert data.get("name") == "service2" and data.get("status") == "OK"
		pass

	def test_service3(self):
		requestBody = { "username": "definately something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8083/", json = requestBody)
		data = response.json()
		assert data.get("name") == "service3" and data.get("status") == "OK"
		pass

	def test_service4(self):
		requestBody = { "username": "something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8084/gatherData", json = requestBody)
		data = response.json()
		assert data == { "name": "service4", "status": "OK" }
		pass


# tests format of response value of all services
class TestResponseValue:
	def test_service0(self):
		response = requests.get("http://127.0.0.1:8080/")
		data = response.json()
		assert isinstance(data.get("data"), list) and all(isinstance(item, list) for item in data.get("data"))
		pass

	def test_service1(self):
		response = requests.get("http://127.0.0.1:8081/")
		data = response.json()
		assert isinstance(data.get("response"), list) and len(data.get("response")) == 2
		pass

	def test_service2(self):
		requestBody = { "username": "with something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8082/", json = requestBody)
		data = response.json()
		assert isinstance(data.get("service4 responses"), list)
		pass

	def test_service3(self):
		requestBody = { "username": "definately something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8083/", json = requestBody)
		data = response.json()
		assert isinstance(data.get("service4 responses"), list)
		pass

	def test_service4(self):
		requestBody = { "username": "something", "content": "some code" }
		response = requests.post("http://127.0.0.1:8084/gatherData", json = requestBody)
		data = response.json()
		assert len(data.keys()) == 2
		pass


# python -m pytest -v
