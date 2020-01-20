from flask import Flask
from threading import Thread
from multiprocessing import Process
import requests
import time
import uuid
import os

__version__ = "1.4"

isWindows = False

if os.name == "nt":
    isWindows = True


class _RunInBackground(object):
    def __init__(self, app, is_alive_route, host=None, port=None):
        self.app = app
        self.host = host
        self.port = port
        self.should_suicide = False
        self.is_alive_route = is_alive_route

        if isWindows:
            Thread(target=self.middleware_thread).start()
        else:
            self.process = Process(target=self.app._run, args=(self.host, self.port))
            self.process.start()

    def middleware_thread(self):
        self.process = Thread(target=self.app._run, args=(self.host, self.port))

        self.process.daemon = True
        self.process.start()

        while True:
            if self.should_suicide:
                break
            time.sleep(0.1)

    def __enter__(self):
        is_alive = False
        first_time = time.time()
        while (time.time() - first_time) < 60:
            try:
                r = requests.put(
                    "http://" + self.host + ":" + str(self.port) + self.is_alive_route
                )
                if r.status_code == 200:
                    is_alive = True
                    break
            except:
                pass
            time.sleep(0.05)

        if not is_alive:
            self.__exit__("", "", "")
            raise Exception("Server isn't alive")

    def __exit__(self, a, b, c):
        if not isWindows:
            self.process.terminate()
        self.should_suicide = True


class HttpServerMock(Flask):
    def __init__(
        self,
        import_name,
        static_url_path=None,
        static_folder="static",
        static_host=None,
        host_matching=False,
        subdomain_matching=False,
        template_folder="templates",
        instance_path=None,
        instance_relative_config=False,
        root_path=None,
        is_alive_route=None,
    ):
        self._run = super().run

        if is_alive_route is None:
            is_alive_route = "/" + str(uuid.uuid1()) + "/" + str(uuid.uuid1())

        self.is_alive_route = is_alive_route
        self.created_alive_route = False
        self._testing_error = False

        return super().__init__(
            import_name,
            static_url_path=static_url_path,
            static_folder=static_folder,
            static_host=static_host,
            host_matching=host_matching,
            subdomain_matching=subdomain_matching,
            template_folder=template_folder,
            instance_path=instance_path,
            instance_relative_config=instance_relative_config,
            root_path=root_path,
        )

    def run(self, host=None, port=None):

        if not self.created_alive_route:
            self.created_alive_route = True

            if not self._testing_error:

                @self.route(self.is_alive_route, methods=["PUT"])
                def is_alive_route_func():
                    return ""

        return _RunInBackground(self, self.is_alive_route, host=host, port=port)
