http-server-mock
================

.. image:: https://img.shields.io/pypi/v/http-server-mock.svg
   :target: https://pypi.python.org/pypi/http-server-mock
   :alt: http-server-mock on PyPI (Python Package Index)

.. image:: https://travis-ci.org/ezequielramos/http-server-mock.svg?branch=master
   :target: https://travis-ci.org/ezequielramos/http-server-mock
   :alt: Travis CI tests (Linux)

.. image:: https://coveralls.io/repos/github/ezequielramos/http-server-mock/badge.svg?branch=master
   :target: https://coveralls.io/github/ezequielramos/http-server-mock?branch=master
   :alt: Test coverage on Coveralls

http-server-mock is a HTTP Server Mock using Flask. You can use it to test possible integrations with your application.

http-server-mock is available on PyPI. To install it just run:
::

    pip install http-server-mock

Using http-server-mock is similar to implement any Flask application.
::

    from http_server_mock import HttpServerMock
    app = HttpServerMock(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return "Hello world"

    with app.run("localhost", 5000):
        r = request.get("/")
        # r.status_code == 200
        # r.text == Hello world 

HttpServerMock will use a random route to know if the http server is running, if you want to set a specific route to do it just set the parameter is_alive_route:
::

    from http_server_mock import HttpServerMock
    app = HttpServerMock(__name__, is_alive_route="/is-alive")