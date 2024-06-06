from flask import Flask, request, jsonify


app = Flask(__name__)


# NEW TASK
@app.route('/new/<details>', methods = ['POST'])
def new_task(details):
    # TODO: add new task
    # header = name
    pass


# GET ALL USERS
@app.route('/users', methods = ['GET'])
def get_users():
    # TODO: return all users
    pass


# UNRECOGNIZED INPUT
@app.route('/error', methods = ['POST'])
def unrecognized():
    # TODO: write/send unrecognized input
    pass


# DELETE TASK
@app.route('/del/<task_id>', methods = ['POST'])
def del_task(task_id):
    # TODO: delete task by it's id
    pass


# LIST ALL TASK FOR USER
@app.route('/list', methods = ['GET'])
def list_tasks():
    # TODO: send all tasks related to a user
    pass


# SEND USER HELP/INSTRUCTIONS
@app.route('/help', methods = ['GET'])
def help():
    # TODO: send help msg explaining commands
    pass

        
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8080, debug = True)