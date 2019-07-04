from main import HttpServerMock
import requests
import time
import unittest

class TestHttpServerMock(unittest.TestCase):
    def test_simple_server(self):

        app = HttpServerMock('test-http-server-mock')

        @app.route("/", methods=["GET"])
        def index_route():
            return 'random text'

        with app.run('localhost', 5000):
            r = requests.get('http://localhost:5000/')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'random text')

        with self.assertRaises(Exception):
            requests.get('http://localhost:5000/')

    def test_simple_server_custom_is_alive_route(self):
        app = HttpServerMock('test-http-server-mock', is_alive_route="/is-alive")
        @app.route("/", methods=["GET"])
        def index_route():
            return 'random text'

        with app.run('localhost', 5000):
            r = requests.get('http://localhost:5000/')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'random text')

        with self.assertRaises(Exception):
            requests.get('http://localhost:5000/')

    def test_running_same_server_multiple_times(self):

        app = HttpServerMock('test-http-server-mock')

        @app.route("/", methods=["GET"])
        def index_route():
            return 'random text'

        with app.run('localhost', 5000):
            r = requests.get('http://localhost:5000/')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'random text')

        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get('http://localhost:5000/')

        with app.run('localhost', 5000):
            r = requests.get('http://localhost:5000/')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'random text')

        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get('http://localhost:5000/')

        with app.run('localhost', 3000):
            r = requests.get('http://localhost:3000/')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'random text')

        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get('http://localhost:3000/')

    def test_multiple_servers(self):

        app = HttpServerMock('test-http-server-mock')
        
        @app.route("/", methods=["GET"])
        def index_route():
            return 'random text'
    
        another_app = HttpServerMock('another-test-http-server-mock')
        @another_app.route("/", methods=["GET"])
        def another_index_route():
            return 'another random text'


        with app.run('localhost', 8000), another_app.run('localhost', 5000):
            r = requests.get('http://localhost:8000/')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'random text')

            r = requests.get('http://localhost:5000/')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'another random text')

        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get('http://localhost:8000/')

        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get('http://localhost:5000/')
