from flask import Flask, request, jsonify
from models.smtp import SMTPbot
from models import fire_db as fire

app = Flask(__name__)
write_email = SMTPbot()



# NEW TASK
@app.route('/new', methods=['POST'])
def new_task():

    user = fire.get_user(request.headers.get('name'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    details = request.json.get('details')
    if not details:
        return jsonify({'error': 'Details not provided'}), 400
    
    task_id = fire.new_task(user['name'], details)
    write_email.new_task(user, task_id, details)

    return jsonify({'message': 'Task created', 'task_id': task_id}), 201


# GET ALL USERS
@app.route('/users', methods = ['GET'])
def get_users():
    users = fire.all_users()
    return jsonify(users), 200


# UNRECOGNIZED INPUT
@app.route('/error', methods = ['POST'])
def unrecognized():

    user = fire.get_user(request.headers.get('name'))
    if not user:
        return jsonify({'error': 'User not found'}), 404

    write_email.error(user)
    return jsonify({'message': 'Unrecognized input error handled'}), 200
    

# DELETE TASK
@app.route('/del/<task_id>', methods = ['DELETE'])
def del_task(task_id):
    
    user = fire.get_user(request.headers.get('name'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    fire.del_task(user['name'], task_id)
    write_email.del_task(user, task_id)
    
    return jsonify({'message': f'Task {task_id} deleted'}), 200


# LIST ALL TASK FOR USER
@app.route('/list', methods = ['GET'])
def list_tasks():

    user = fire.get_user(request.headers.get('name'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    tasks = fire.list_tasks(user['name'])
    write_email.list_tasks(user, tasks)
    
    return jsonify({'tasks': tasks}), 200


# SEND USER HELP/INSTRUCTIONS
@app.route('/help', methods = ['GET'])
def help():
    
    user = fire.get_user(request.headers.get('name'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    write_email.help(user)
    return jsonify({'message': 'Help instructions sent'}), 200


@app.route('/remind', methods = ['GET'])
def reminder():


    pass

        
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8080, debug = True)