from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
from tools.manager import Manager


app = Flask(__name__)
manager = Manager()
standart_date = datetime.strptime('2001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')


@app.route('/', methods=['GET'] )
def indexGET():
    task_list = manager.getTasks()
    return render_template('index.html', tasks=task_list, standart_date=str(standart_date) )


@app.route("/task/add", methods=["POST"])
def addTask():
    data = request.get_json()
    task = data.get("task")

    if not task:
        return {"error": "No task"}

    date_created = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_item = manager.addTask(task, date_created)

    return jsonify(new_item)


@app.route("/task/remove", methods=["POST"])
def removeTask():
    data = request.get_json()
    id = data.get("id")

    if not id:
        return {"error": "No id"}

    removed = manager.removeTask(id)

    return removed


@app.route("/task/update", methods=["POST"])
def updateTask():
    data = request.get_json()
    id = data.get('id')
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    if not id:
        return jsonify({"error": "No id"})
    
    updated = manager.updateTask(id, date)

    return jsonify(updated)


if __name__ == '__main__':
    app.run(debug=True)