from flask import Flask, request, jsonify
from cloud_run.src.models.smtp import SMTPbot
from cloud_run.src.database import fire_db as fire

app = Flask(__name__)
write_email = SMTPbot()

# NEW TASK
@app.route('/new/<details>', methods = ['POST'])
def new_task(details):

    user = fire.get_user(request.headers.get('name'))
    task_id = fire.new_task(user.name, details)

    write_email.new_task(user, task_id, details)


# GET ALL USERS
@app.route('/users', methods = ['GET'])
def get_users():

    return jsonify(fire.all_users())


# UNRECOGNIZED INPUT
@app.route('/error', methods = ['POST'])
def unrecognized():

    user = fire.get_user(request.headers.get('name'))

    write_email.error(user)
    

# DELETE TASK
@app.route('/del/<task_id>', methods = ['POST'])
def del_task(task_id):
    
    user = fire.get_user(request.headers.get('name'))
    fire.del_task(user.name, task_id)

    write_email.del_task(user.name, task_id)
    


# LIST ALL TASK FOR USER
@app.route('/list', methods = ['GET'])
def list_tasks():

    user = fire.get_user(request.headers.get('name'))
    tasks = fire.list_tasks(user.name)

    write_email.list_tasks(user, tasks)


# SEND USER HELP/INSTRUCTIONS
@app.route('/help', methods = ['GET'])
def help():
    
    user = fire.get_user(request.headers.get('name'))

    write_email.help(user)

        
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8080, debug = True)