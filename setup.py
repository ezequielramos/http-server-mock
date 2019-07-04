"""Run "python setup.py install" to install http_server_mock."""

import os
import re
import sys
from distutils.core import setup


open_args = {"encoding": "utf-8"}


with open(
    os.path.join(os.path.dirname(__file__), "http_server_mock.py"), **open_args
) as f:
    for line in f:
        match = re.match(r"__version__.*\"([0-9.]+)\"", line)
        if match:
            version = match.group(1)
            break
    else:
        raise Exception("Couldn't find __version__ line in http_server_mock.py")


# Read long_description from README.rst
with open(os.path.join(os.path.dirname(__file__), "README.rst"), **open_args) as f:
    long_description = f.read()


setup(
    name="http_server_mock",
    version=version,
    author="Ezequiel Ramos",
    author_email="ezequielmr94@gmail.com",
    url="https://github.com/ezequielramos/http-server-mock",
    license="GNU General Public License v3.0",
    description="Python 3 library to mock a http server using Flask",
    long_description=long_description,
    py_modules=["http_server_mock"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=["flask", "requests"],
)
