from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_HOST = os.getenv('MONGO_HOST', 'mongo')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client.todo_db
coll = db.tasks

@app.route('/')
def index():
    tasks = list(coll.find({}, {'_id': 0}))
    return render_template('index.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = list(coll.find({}, {'_id': 0}))
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'task' not in data:
        return jsonify({'error': 'task required'}), 400
    coll.insert_one({'task': data['task'], 'completed': False})
    return jsonify({'status': 'ok'}), 201

@app.route('/api/tasks/<string:task_name>', methods=['DELETE'])
def delete_task(task_name):
    coll.delete_one({'task': task_name})
    return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

