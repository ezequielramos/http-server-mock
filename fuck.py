from main import HttpServerMock
import requests

app = HttpServerMock('test-http-server-mock')

@app.route("/", methods=["GET"])
def index_route():
    return 'random text'

with app.run('localhost', 5000):
    r = requests.get('http://localhost:5000/')
    print(r.status_code, 200)
    print(r.text, 'random text')
