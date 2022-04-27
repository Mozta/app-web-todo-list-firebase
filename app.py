from flask import Flask, redirect, render_template, request
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

app = Flask(__name__)
# Configuraciones para firebase
cred = credentials.Certificate('serviceAccountKey.json')
fire = firebase_admin.initialize_app(cred)
db = firestore.client()
tasks_ref = db.collection('tasks')
users_ref = db.collection('users')
API_KEY = 'AIzaSyDpWOwvHcvnL3aamIZpUwvORgFaST8lI_4'


def read_tasks(ref):
    docs = ref.get()
    all_tasks = []
    for doc in docs:
        task = doc.to_dict()
        task['id'] = doc.id
        all_tasks.append(task)
    return all_tasks

def create_task(ref, task):
    new_task = {'name':task, 
            'check':False, 
            'fecha': datetime.datetime.now()}
    ref.document().set(new_task)

def update_task(ref,id):
    ref.document(id).update({'check':True})

def delete_task(ref, id):
    res = ref.document(id).delete()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        try:
            tasks = read_tasks(tasks_ref)
            completed = []
            incompleted = []
            for task in tasks:
                print(task['check'])
                if task['check'] == True:
                    completed.append(task)
                else:
                    incompleted.append(task)
        except:
            print("Error...")
            tasks = []

        response = {'completed':completed, 
                    'incompleted':incompleted,
                    'counter1':len(completed),
                    'counter2':len(incompleted)}
        return render_template('index.html', response=response)
    else: #POST
        name = request.form["name"]
        print(f"\n{name}\n")
        try:
            create_task(tasks_ref, name)
            return redirect('/')
        except:
            return render_template('error.html', response='response')

@app.route("/update/<string:id>", methods=['GET'])
def update(id):
    print(f"\nVas a actualizar la tarea: {id}\n")
    try:
        update_task(tasks_ref,id)
        return redirect('/')
    except:
        return render_template('error.html', response='response')

@app.route("/delete/<string:id>", methods=['GET'])
def delete(id):
    print(f"\nVas a borrar la tarea: {id}\n")
    
    try:
        delete_task(tasks_ref, id)
        print("Tarea eliminada...")
        return redirect('/')
    except:
        return render_template('error.html', response='response')

if __name__ == '__main__':
    app.run(debug=True)