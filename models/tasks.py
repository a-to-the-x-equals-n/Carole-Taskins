import time

class Tasks:

    def __init__(self, owner, details, assignee = None, due = None):
        self.owner = owner
        self.timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.today = time.strftime("%-m/%d/%Y", time.localtime())
        self.details = details
        self.assignee = assignee
        self.due = due
        self.id = self.today.replace('/', '') + '-' + self.timestamp.replace(':','')




if __name__ == "__main__":
    # Example usage
    test = Tasks("Logan", "This is just a test.", "Bianca")

    print(f'{test.id}')