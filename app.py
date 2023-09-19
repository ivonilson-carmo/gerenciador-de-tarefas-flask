from flask import Flask, render_template, request, redirect
from datetime import datetime
from tools.manager import Manager


app = Flask(__name__)
manager = Manager()
standart_date = datetime.strptime('2001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')


@app.route('/', methods=['POST'])
def indexPOST():
    task = request.form['text-task']
    date_created = datetime.now().strftime('%Y-%m-%d %H:%M')

    manager.addTask(task, date_created)

    return redirect('/')


@app.route('/', methods=['GET'] )
def indexGET():
    task_list = manager.getTasks()
    return render_template('index.html', tasks=task_list, standart_date=str(standart_date) )

@app.route('/check', methods=['POST'])
def checkTask():
    identify = request.form.getlist('check-task')
    date = datetime.now().strftime('%Y-%m-%d %H:%M')

    if identify:
        manager.checkTask(identify[0], date)

    return redirect('/')

@app.route('/remove', methods=['post'])
def removeTasks():
    identify = request.form['identify']

    manager.removeTask(identify)

    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)