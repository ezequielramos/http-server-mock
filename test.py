from main import HttpServerMock
import requests
import time

app = HttpServerMock(__name__)

@app.route("/", methods=["GET"])
def hello():
    return 'vitoria ou nem'

with app.run('localhost', 5000):
    r = requests.get('http://localhost:5000/')
    print(r.status_code, r.text)

with app.run('localhost', 3000):
    r = requests.get('http://localhost:3000/')
    print(r.status_code, r.text)

app2 = HttpServerMock(__name__, is_alive_route="/is-alive")

@app2.route("/", methods=["GET"])
def hello2():
    return 'vitoria ou nem'

with app2.run('localhost', 8000):
    r = requests.get('http://localhost:8000/')
    print(r.status_code, r.text)


r = requests.get('http://localhost:5000/')
r = requests.get('http://localhost:3000/')
r = requests.get('http://localhost:8000/')