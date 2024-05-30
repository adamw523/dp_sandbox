from flask import Flask
import random


app = Flask(__name__)


@app.get("/healthcheck")
def readiness_probe():
    return "I'm ready!"


@app.post("/randint")
@app.get("/randint")
def randint():
    return str(random.randint(1, 100))


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
