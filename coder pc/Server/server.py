
from .api import run_server
from .database import db


def start_server(host="0.0.0.0", port=5000):
    db.connect()
    db.initialize_tables()
    run_server(host, port)


def stop_server():
    db.disconnect()
