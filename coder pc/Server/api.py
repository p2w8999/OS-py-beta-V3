
from flask import Flask, jsonify, request
from .database import db
from OS.kernel import kernel
import threading


app = Flask(__name__)


@app.route("/api/kernel/status", methods=["GET"])
def kernel_status():
    return jsonify({
        "status": "running" if kernel.running else "stopped",
        "uptime": kernel.get_uptime()
    })


@app.route("/api/kernel/boot", methods=["POST"])
def kernel_boot():
    kernel.boot()
    return jsonify({"message": "Kernel booted successfully"})


@app.route("/api/kernel/shutdown", methods=["POST"])
def kernel_shutdown():
    kernel.shutdown()
    return jsonify({"message": "Kernel shut down successfully"})


@app.route("/api/processes", methods=["GET"])
def list_processes():
    return jsonify(kernel.process_manager.list_processes())


@app.route("/api/processes", methods=["POST"])
def create_process():
    data = request.json
    name = data.get("name", "unnamed-process")
    # For demo, create a simple process that sleeps
    import time
    pid = kernel.process_manager.create_process(name, lambda: time.sleep(10))
    kernel.process_manager.start_process(pid)
    return jsonify({"pid": pid, "message": "Process created and started"})


@app.route("/api/processes/<pid>", methods=["DELETE"])
def terminate_process(pid):
    success = kernel.process_manager.terminate_process(pid)
    if success:
        return jsonify({"message": "Process terminated"})
    return jsonify({"error": "Process not found"}), 404


@app.route("/api/filesystem/<path:path>", methods=["GET"])
def read_file(path):
    content = kernel.file_system.read_file(path)
    if content is not None:
        return jsonify({"content": content})
    return jsonify({"error": "File not found"}), 404


@app.route("/api/filesystem/<path:path>", methods=["POST"])
def write_file(path):
    data = request.json
    content = data.get("content", "")
    kernel.file_system.write_file(path, content)
    return jsonify({"message": "File written successfully"})


@app.route("/api/filesystem/<path:path>", methods=["DELETE"])
def delete_file(path):
    success = kernel.file_system.delete_file(path)
    if success:
        return jsonify({"message": "File deleted"})
    return jsonify({"error": "File not found"}), 404


@app.route("/api/filesystem/list/<path:path>", methods=["GET"])
def list_directory(path):
    return jsonify({"items": kernel.file_system.list_directory(path)})


@app.route("/api/users", methods=["GET"])
def get_users():
    users = db.fetch_all("SELECT id, username, email, created_at FROM users")
    return jsonify([{"id": u[0], "username": u[1], "email": u[2], "created_at": u[3]} for u in users])


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    if not username or not email:
        return jsonify({"error": "Username and email required"}), 400
    db.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
    return jsonify({"message": "User created successfully"}), 201


@app.route("/api/logs", methods=["GET"])
def get_logs():
    logs = db.fetch_all("SELECT id, level, message, created_at FROM logs ORDER BY created_at DESC")
    return jsonify([{"id": l[0], "level": l[1], "message": l[2], "created_at": l[3]} for l in logs])


@app.route("/api/logs", methods=["POST"])
def add_log():
    data = request.json
    level = data.get("level", "info")
    message = data.get("message")
    if not message:
        return jsonify({"error": "Message required"}), 400
    db.execute("INSERT INTO logs (level, message) VALUES (?, ?)", (level, message))
    return jsonify({"message": "Log added successfully"}), 201


def run_server(host="0.0.0.0", port=5000):
    app.run(host=host, port=port, debug=False, threaded=True)
