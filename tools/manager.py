from datetime import datetime
import sqlite3



class Manager:
    def __init__(self):
        self.filename = 'storage.db'
        self.db , self.cursor = self.connect()

        # cria tabela(se não tiver criada ainda)
        self.makeTable()


    def connect(self):
        """ Realiza conexão com banco de dados """
        db = sqlite3.connect(self.filename, check_same_thread=False)
        cursor = db.cursor()

        return [db, cursor]

    
    def makeTable(self):
        """ cria a base da tabela se não existir """

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT(30),
                email TEXT(50),
                senha TEXT(50),
                created_at DATETIME
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                task TEXT NOT NULL,
                created_at DATETIME,
                completed_at DATETIME,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            ''')
        
        self.saveDB()
    
    def checkLogin(self, email, senha):
        script = f'SELECT id, username FROM users WHERE email = "{email}" AND senha = "{senha}"'
        search = self.cursor.execute(script).fetchone()
        if search:
            user_id, user = search

            return {
                'user_id':user_id,
                'username': user
            }
        
        return
    
    def checkEmail(self, email):
        script = f'SELECT email FROM users WHERE email = "{email}"'
        search = self.cursor.execute(script)

        return search.fetchone()

    def checkUser(self, user):
        script = f'SELECT username FROM users WHERE username = "{user}"'
        search = self.cursor.execute(script)

        return search.fetchone()
    
    def addUser(self, user, email, senha):
        """ Adciona novo usuario no sistema """
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        checkEmail = self.checkEmail(email)
        if checkEmail:  # verifica se já existe o email
            return {'error': 'E-mail já existente, faça login ou utilize outro!'}
        
        checkUser = self.checkUser(user)
        if checkUser:
            return {'error': 'Nome de usuário não está disponível, tente novamente!'}
        
        script = 'INSERT INTO users (username, email, senha, created_at)  VALUES (?, ?, ?, ?)'
        exec_script = self.cursor.execute(script, (user, email, senha, date))

        self.saveDB()

        return { 'user_id': exec_script.lastrowid }

    
    def addTask(self, task, created_at, user_id):
        """ Adciona registro de tarefa no sistema """

        script = 'INSERT INTO tasks (task, created_at, completed_at, user_id) VALUES(?, ?, ?, ?)'
        exec_script = self.cursor.execute(script, [task, created_at, None, user_id] )
        
        self.saveDB()

        return {
            'task': task,
            'created_at': created_at,
            'identify': exec_script.lastrowid
        }
    
    def findByID(self, identify, user_id):
        """ Busca se existe o `identify` na tabela"""
        search = self.cursor.execute(f'SELECT id FROM tasks WHERE id = {identify} AND user_id == {user_id}')
        return search.fetchone()

    def updateTask(self, identify, date, user_id):
        """ Marca tarefa como concluida """
        script = f'UPDATE tasks SET completed_at = "{date}" WHERE id = {identify} AND user_id = {user_id}'
        
        if self.findByID(identify, user_id):
            self.cursor.execute(script)
            self.saveDB()

            return {'completed_at': date}
        
        return {'error': 'not found id'}
    
    def removeTask(self, identify, user_id):
        """ remove registro de tarefa através do id"""
        if self.findByID(identify, user_id):
            self.cursor.execute(f'DELETE FROM tasks WHERE id={identify} AND user_id = {user_id}')
            self.saveDB()

            return {'identify': identify}
    
        return {'error': 'not found id'}
        
    
    def saveDB(self):
        """ Salva registros no banco de dados """
        self.db.commit()
        self.cursor.close()
        
        self.db, self.cursor = self.connect()
    
    def getTasksUser(self, user_id):
        """ Retorna todas tarefas do banco de dados numa lista
         sendo primeiro as tarefas comuns e após isso as que ja foram concluidas  """

        # busca das tarefas que nao foram concluida
        activeTasks = self.cursor.execute(f'SELECT * FROM tasks WHERE completed_at IS NULL AND user_id = {user_id} ')
        result = activeTasks.fetchall()
        
        # busca as tarefas que foram concluidas
        finishedTasks = self.cursor.execute(f'SELECT * FROM tasks WHERE completed_at IS NOT NULL AND  user_id = {user_id}')
        result += finishedTasks.fetchall()

        return result 
