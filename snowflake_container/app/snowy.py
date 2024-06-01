from flask import Flask, make_response
import random


app = Flask(__name__)


@app.get("/healthcheck")
def readiness_probe():
    return "I'm ready!"


@app.post("/randint")
@app.get("/randint")
def randint():
    response = make_response({"data": [[0, random.randint(1, 100)]]})
    response.headers["Content-type"] = "application/json"
    return response


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
