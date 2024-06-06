from google.cloud import firestore

# Initialize Firestore
db = firestore.Client()

# Function to fetch the highest task ID for a user and determine the next ID
def get_next_task_id(user_doc_ref):
    user_doc = user_doc_ref.get()
    if user_doc.exists:
        tasks = user_doc.to_dict().get("tasks", [])
        if tasks:
            max_id = max(int(task["id"]) for task in tasks)
            return str(max_id + 1).zfill(3)  # zero-fill for consistent ID format
    return "001"

# Function to add a task for a user with auto-incremented ID
def add_task_for_user(user_name, task_details):
    user_doc_ref = db.collection('users').document(user_name)
    next_task_id = get_next_task_id(user_doc_ref)
    new_task = {
        "id": next_task_id,
        "details": task_details
    }
    user_doc_ref.update({
        "tasks": firestore.ArrayUnion([new_task])
    })

# Adding tasks to users
def add_users_tasks(users_tasks):
    for user in users_tasks:
        user_doc_ref = db.collection('users').document(user["name"])
        user_doc_ref.set({"name": user["name"], "tasks": []}, merge=True)
        for task in user["tasks"]:
            add_task_for_user(user["name"], task["details"])

# List of users and their initial tasks
users_tasks = [
    {
        "name": "Dan",
        "tasks": [
            {
                "details": "Work order for left oven"
            },
            {
                "details": "Replace filter in HVAC system"
            }
        ]
    },
    {
        "name": "Mark",
        "tasks": [
            {
                "details": "Check inventory in storage"
            }
        ]
    }
]

if __name__ == "__main__":
    add_users_tasks(users_tasks)
    print("User tasks have been added to Firestore.")
