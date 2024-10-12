import requests as reqs
from flask import Flask, request, jsonify
from task_model import Task_model

app = Flask(__name__)
api_route = "/v1/tasks"

@app.route(api_route, methods=["POST"])
def create_task_s():
    db = Task_model()
    data = request.get_json()
    resp = []
    status = 400
    if "tasks" in data:
        for task in data["tasks"]:
            id = db.add_task(task)
            resp.append({"id": id})
        status = 201
    elif "title" in data:
        id = db.add_task(data)
        resp = {"id": id}
        status = 201
    return jsonify(resp), status

@app.route(api_route, methods=["GET"])
def list_all_tasks():
    db = Task_model()
    data = db.get_all_task()
    return jsonify(data), 200

@app.route(f"{api_route}/<int:tid>", methods=["GET"])
def retrieve(tid):
    db = Task_model()
    data, status = db.get_task(tid)
    return jsonify(data), status

@app.route(f"{api_route}/<int:tid>", methods=["PUT"])
def update(tid):
    db = Task_model()
    new_data = request.get_json()
    data, status = db.update_task(tid, new_data)
    return jsonify(data), status

@app.route(f"{api_route}/<int:tid>", methods=["DELETE"])
def delete(tid):
    db = Task_model()
    data, status = db.delete_task(tid)
    return jsonify(data), status

# Extras
@app.route(api_route, methods=["DELETE"])
def delete_bulk():
    db = Task_model()
    data = request.get_json()
    status = 204
    if "tasks" in data:
        for task_id in data["tasks"]:
            status = db.delete_task(task_id)
    return jsonify(None), status

if __name__ == '__main__':
    app.run(debug=True)
