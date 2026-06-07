from flask import Flask, jsonify, make_response
from mcstatus import JavaServer
import time

app = Flask(__name__)

SERVER_ADDRESS = "email-treasure.gl.joinmc.link"
SERVER_PORT = 25565

start_time = time.time()


def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, ngrok-skip-browser-warning"
    return response


@app.after_request
def after_request(response):
    return add_cors_headers(response)


@app.route("/")
def home():
    return "Ponkan Server API is running!"


@app.route("/status", methods=["GET", "OPTIONS"])
def status():
    if flask_request_is_options():
        response = make_response("", 200)
        return add_cors_headers(response)

    try:
        server = JavaServer.lookup(f"{SERVER_ADDRESS}:{SERVER_PORT}")
        data = server.status()

        response = jsonify({
            "online": True,
            "players": data.players.online,
            "maxPlayers": data.players.max,
            "version": data.version.name,
            "latency": round(data.latency),
            "uptimeSeconds": int(time.time() - start_time)
        })

        return response

    except Exception as e:
        response = jsonify({
            "online": False,
            "players": 0,
            "maxPlayers": 0,
            "version": "不明",
            "latency": None,
            "uptimeSeconds": int(time.time() - start_time),
            "error": str(e)
        })

        return response


def flask_request_is_options():
    from flask import request
    return request.method == "OPTIONS"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)