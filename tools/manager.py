from datetime import datetime
import sqlite3



class Manager:
    def __init__(self):
        # nome do arquivo de banco de dados
        self.filename = 'storage.db'

        # realiza a conexão com o banco de dados 
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
        script = '''
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            task TEXT NOT NULL,
            date_created DATETIME,
            date_finished DATETIME
            );'''
        self.cursor.execute(script)
        self.saveDB()
    
    def addTask(self, task, date_created):
        """ Adciona registro de tarefa no sistema """
        date = datetime.strptime('2001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

        script = 'INSERT INTO tasks (task, date_created, date_finished) VALUES (?, ?, ?)'
        self.cursor.execute(script, (task, date_created, None))
        self.saveDB()
    
    def checkTask(self, identify, date):
        """ Marca tarefa como concluida """
        script = f'UPDATE tasks SET date_finished = "{date}" WHERE id = {identify}'
        
        self.cursor.execute(script)
        self.saveDB()
    
    def removeTask(self, identify):
        """ remove registro de tarefa através do id"""
        script = f'DELETE FROM tasks WHERE id={identify}'
        self.cursor.execute(script)

        self.saveDB()
    
    def saveDB(self):
        """ Salva registros no banco de dados """
        self.db.commit()
        self.cursor.close()
        
        self.db, self.cursor = self.connect()
    
    def getTasks(self):
        """ Retorna todas tarefas do banco de dados numa lista
         sendo primeiro as tarefas comuns e após isso as que ja foram concluidas  """

        # busca das tarefas que nao foram concluida
        activeTasks = self.cursor.execute('SELECT * FROM tasks WHERE date_finished IS NULL ')
        result = activeTasks.fetchall()
        # busca as tarefas que foram concluidas
        finishedTasks = self.cursor.execute('SELECT * FROM tasks WHERE date_finished IS NOT NULL')
        result += finishedTasks.fetchall()

        return result 
    