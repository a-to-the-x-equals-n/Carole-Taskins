from google.cloud import firestore
from util import load_vars


PROJECT, DATABASE = load_vars("PROJECT_ID", "DATABASE")
# GOOGLE_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS').replace('wsl.localhost/Ubuntu/', "")
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS
# print(f'{GOOGLE_CREDENTIALS}')
db = firestore.Client(project = PROJECT, database = DATABASE) # Initialize Datastore client


def get_user(name):
    user = db.collection('users').where('name', '==', name).limit(1).get()[0]
    user_dict = user.to_dict()
    user_dict['id'] = user.id
    return user_dict
    


# Function to fetch all users
def all_users():
    user_collection = db.collection('users').stream()   # Retrieve all documents in the 'users' collection as a stream
    all_users = {}                                      # Initialize an empty dictionary to store all users

    # Iterate over each user document in the collection
    for user in user_collection:

        user_dict = user.to_dict()      # Convert each user document to a dictionary
        all_users[user.id] = user_dict  # Use the document ID as the key in the dictionary
    
    return all_users


# Get a masterlist of a users tasks
def list_tasks(name):
    user_document_reference = db.collection('task_collection').document(name)   # Reference to the user document in the 'task_collection' collection
    tasks_collection_reference = user_document_reference.collection('tasks')    # Reference to the 'tasks' subcollection within the user document
    tasks_collection = tasks_collection_reference.stream()                      # Get all task documents
    
    # Create dictionary to store 'name' and 'tasks'
    user_task_list = {
        'tasks': []     # Initialize an empty list to store tasks
    }
    
    # Iterate over each task document
    for task_doc in tasks_collection:
    
        task_dict = task_doc.to_dict()              # Convert task document to dictionary
        task_dict['id'] = task_doc.id               # Add task ID
        user_task_list['tasks'].append(task_dict)   # Append task data to the 'tasks' list in the result dictionary
    
    return user_task_list


# Add a new task to a user's task subcollection
def new_task(name, details):
    # Database operations
    user_document_reference = db.collection('task_collection').document(name)  # Reference to the user document in the 'task_collection' collection
    tasks_collection_reference = user_document_reference.collection('tasks')   # Reference to the 'tasks' subcollection within the user document
    task_collection = tasks_collection_reference.stream()                      # Get all task documents in the 'tasks' subcollection
    
    # Max_id variable to track highest ID
    max_id = 0
    
    # Iterate over each task document to find the highest task ID
    for task in task_collection:
        id = int(task.id)
        max_id = id if id > max_id else max_id
    
    # Increment the highest task ID to get the new task ID
    new_task_id = str(max_id + 1).zfill(3)  # Zero-fill to maintain three-digits
    
    # Create the new task data
    new_task_data = {
        'details': details
    }
    
    new_task_document_reference = tasks_collection_reference.document(new_task_id)  # Reference to the new task document using the new task ID
    new_task_document_reference.set(new_task_data)                                  # Set the new task data in the Firestore document

    return new_task_id

# Delete a task by user name and task ID
def del_task(name, id):
    user_document_reference = db.collection('task_collection').document(name)           # Reference to the user document in the 'task_collection' collection
    task_document_reference = user_document_reference.collection('tasks').document(id)  # Reference to the specific task document in the 'tasks' subcollection
    task_document_reference.delete()                                                    # Delete task




if __name__ == "__main__":
    name = "logan"
    #3 new_task(name, "inventory")
    del_task(name, "002")
