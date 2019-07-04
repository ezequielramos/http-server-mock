from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
x = lambda a : a + 10