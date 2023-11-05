from flask import Flask, render_template, request, redirect, jsonify, session
from datetime import datetime
from tools.manager import Manager


app = Flask(__name__)
app.secret_key = '123456'

manager = Manager()


@app.route('/', methods=['GET'] )
def indexGET():
    if 'user' in session:
        task_list = manager.getTasksUser(session['user_id'])
        print(task_list)
        return render_template('index.html', tasks=task_list )
    
    return redirect('login')


@app.route("/task/add", methods=["POST"])
def addTask():
    data = request.get_json()
    task = data.get("task")

    if not task:
        return {"error": "No task"}

    date_created = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_item = manager.addTask(task, date_created, session['user_id'])

    return jsonify(new_item)


@app.route("/task/remove", methods=["POST"])
def removeTask():
    data = request.get_json()
    id = data.get("id")

    if not id:
        return {"error": "No id"}

    removed = manager.removeTask(id, user_id=session['user_id'])

    return removed


@app.route("/task/update", methods=["POST"])
def updateTask():
    data = request.get_json()
    id = data.get('id')
    date = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    if not id:
        return jsonify({"error": "No id"})
    
    updated = manager.updateTask(id, date, session['user_id'])

    return jsonify(updated)

@app.route('/cadastro')
def getCadastro():
    if 'user' in session:
        return redirect('/')
    return render_template('cadastro.html')

@app.route('/user/cadastro', methods=['POST'])
def postCadastro():
    dados = request.get_json()
    user, email, passwd = dados.get('user'), dados.get('email'), dados.get('passwd')
    if (user and email and passwd):

        data = manager.addUser(user, email, passwd)

        if 'error' in data:
            return data

        session["user"] = user
        session["email"] = email
        session["passwd"] = passwd
        session['user_id'] = data['user_id']

        return jsonify({'status': 'done'})

    return jsonify({ 'error': 'Dados faltantes ' })


@app.route('/user/login', methods=['POST'])
def postLogin():
    dados = request.get_json()
    email, passwd = dados.get('email'), dados.get('passwd')
    
    if (email and passwd):
        check_login = manager.checkLogin(email, passwd)
        if check_login:
            session['email'] = email
            session['passwd'] = passwd
            session['user'] = check_login['username']
            session['user_id'] = check_login['user_id']

            return jsonify({ 'status': 'done' })
        
        return jsonify({ "error": "dados incorretos "})

    
    return jsonify({ "error": "dados faltantes "})


@app.route('/login')
def getLogin():
    if 'user' in session:
        return redirect('/')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user')
    session.pop('email')
    session.pop('passwd')
    session.pop('user_id')

    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)