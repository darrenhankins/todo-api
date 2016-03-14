""" http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
$ mkdir todo-api
$ cd todo-api
$ virtualenv flask
New python executable in flask/bin/python
Installing setuptools............................done.
Installing pip...................done.
$ flask/bin/pip install flask
$ pip install flask-httpauth

$ chmod a+x app.py
$ ./app.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader

Won't run using $ ./app.py
use
$ python app.py
 """

#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
# pip install flask-httpauth (installs module named flask.ext.httpauth)
from flask.ext.httpauth import HTTPBasicAuth

# app = Flask(__name__)
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

# $ curl -u username:password -i http://localhost:5000/todo/api/v1.0/tasks
# authorizing a user
@auth.get_password
def get_password(username):
    if username == 'username':
        return 'password'
    return None

# tasks list
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

# error handling using jsonify instead of a html response
# id 3 does not exist
# $ curl -i http://localhost:5000/todo/api/v1.0/tasks/3
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

# get tasks based on URI
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

# get all tasks
# $ curl -i http://localhost:5000/todo/api/v1.0/tasks
# $ curl -u username:password -i http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

# get specific tasks
# $ curl -i http://localhost:5000/todo/api/v1.0/tasks/2
# $ curl -u username:password -i http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# create a new task
# $ curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Write a letter"}' http://localhost:5000/todo/api/v1.0/tasks
# $ curl -u username:password -i -H "Content-Type: application/json" -X POST -d '{"title":"Write a letter"}' http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

# update task
# $ curl -i -H "Content-Type: application/json" -X PUT -d '{"description":"This is a test","done":false}' http://localhost:5000/todo/api/v1.0/tasks/2
# $ curl -u username:password -i -H "Content-Type: application/json" -X PUT -d '{"description":"This is a test","done":false}' http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# delete a specific task
# $ curl -i -X "DELETE" http://localhost:5000/todo/api/v1.0/tasks/2
# $ curl -u username:password -i -X "DELETE" http://localhost:5000/todo/api/v1.0/tasks/2
# $ man curl  (to list curl commands, exit with control+z)
# -i is a curl command: (HTTP) Include the HTTP-header in the  output
# -X, --request <command> (HTTP) Specifies a custom request method to use when communicating  with the HTTP server. Common additional HTTP requests include PUT and DELETE
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task =[task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
