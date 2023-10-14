from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
from tools.manager import Manager


app = Flask(__name__)
manager = Manager()
standart_date = datetime.strptime('2001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')


@app.route('/', methods=['POST'])
def indexPOST():
    if request.form.get('action'):
        action = request.form['action']

        if action == 'add':
            task = request.form.get('task')
            date_created = datetime.now().strftime('%Y-%m-%d %H:%M')
            new_item = manager.addTask(task, date_created)

            data = {
                'task':task,
                'date_created': date_created,
                'identify': new_item,
            }


            return jsonify(data)
        
        elif action == 'remove':
            identify = int(request.form['identify'])
            manager.removeTask(identify)

            return jsonify({})
        
        elif action == 'check':
            date = datetime.now().strftime('%Y-%m-%d %H:%M')
            identify = int(request.form['identify'])

            manager.checkTask(identify, date)

            return jsonify({
                'date': str(date),
            })
    else:
        return ''




@app.route('/', methods=['GET'] )
def indexGET():
    task_list = manager.getTasks()
    return render_template('index.html', tasks=task_list, standart_date=str(standart_date) )



if __name__ == '__main__':
    app.run(debug=True)