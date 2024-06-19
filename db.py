from google.cloud import firestore
import os
from dotenv import load_dotenv
from pathlib import Path
import os
import asyncio


try:
    # Determine the current directory of the script and locate the .env file
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    envars = current_dir / ".env"
    # Load the environment variables from the .env file
    load_dotenv(envars)
# If any exception occurs during the process, raise an EnvFileError
except Exception as e:
    print(f'Error opening .env file: {str(e)}')


PROJECT = os.getenv("PROJECT_ID")
DATABASE = os.getenv("DATABASE")
CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS

db = firestore.Client(project = PROJECT, database = DATABASE) # Initialize Datastore client

async def get_user(name):
    user = db.collection('users').where('name', '==', name).limit(1).get()[0]
    user_dict = user.to_dict()
    return user_dict
    


# Function to fetch all users
async def all_users():
    user_collection = db.collection('users').stream()   # Retrieve all documents in the 'users' collection as a stream
    all_users = []                                      # Initialize an empty dictionary to store all users

    # Iterate over each user document in the collection
    for user in user_collection:

        user_dict = user.to_dict()      # Convert each user document to a dictionary
        all_users.append(user_dict)  # Use the document ID as the key in the dictionary
    
    return all_users


# Get a masterlist of a users tasks
async def list_tasks(name):
    user_document_reference = db.collection('task_collection').document(name)   # Reference to the user document in the 'task_collection' collection
    tasks_collection_reference = user_document_reference.collection('tasks')    # Reference to the 'tasks' subcollection within the user document
    tasks_collection = tasks_collection_reference.stream()                      # Get all task documents
    
    # Create dictionary to store 'name' and 'tasks'
    user_task_list = []
    
    # Iterate over each task document
    for task_doc in tasks_collection:
    
        task_dict = task_doc.to_dict()              # Convert task document to dictionary
        task_dict['id'] = task_doc.id               # Add task ID
        user_task_list.append(task_dict)   # Append task data to the 'tasks' list in the result dictionary
    
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
async def del_task(name, id):
    user_document_reference = db.collection('task_collection').document(name)           # Reference to the user document in the 'task_collection' collection
    task_document_reference = user_document_reference.collection('tasks').document(id)  # Reference to the specific task document in the 'tasks' subcollection
    task_document_reference.delete()    


if __name__ == "__main__":
    name = "logan"
    new_task(name, "inventory")
    # del_task(name, "002")
