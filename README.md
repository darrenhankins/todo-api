# todo-api
#### RESTful API with Python and Flask

http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


#### Start the API
Open up terminal window, run
``` bash
$ python app.py
```
Running on http://127.0.0.1:5000/

Since this RESTful API requires an authorized user. Opens up another terminal window, run command below. Should result in a list of tasks.
``` bash
curl -u username:password -i http://localhost:5000/todo/api/v1.0/tasks
```
##### Additional Commands
Get specific task (2)
``` bash
curl -i http://localhost:5000/todo/api/v1.0/tasks/2
```

Get all tasks
``` bash
curl -u username:password -i http://localhost:5000/todo/api/v1.0/tasks @app.route('/todo/api/v1.0/tasks', methods=['GET'])
```

Create new task
``` bash
curl -u username:password -i -H "Content-Type: application/json" -X POST -d '{"title":"Write a letter"}' http://localhost:5000/todo/api/v1.0/tasks
```

Update task (2)
``` bash
curl -u username:password -i -H "Content-Type: application/json" -X PUT -d '{"description":"This is a test","done":false}' http://localhost:5000/todo/api/v1.0/tasks/2
```

Delete a task (2)
``` bash
curl -u username:password -i -X "DELETE" http://localhost:5000/todo/api/v1.0/tasks/2
```
