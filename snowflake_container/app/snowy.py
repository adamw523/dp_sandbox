from flask import Flask

app = Flask(__name__)


@app.get("/healthcheck")
def readiness_probe():
    return "I'm ready!"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
