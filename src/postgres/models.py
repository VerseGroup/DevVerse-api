class User():
    def __init__(self, username, email, phone, display_name, github_oauth_token):
        self.username = username
        self.email = email
        self.phone = phone
        self.display_name = display_name
        self.github_oauth_token = github_oauth_token

    def serialize(self):
        return {
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'display_name': self.display_name,
            'github_oauth_token': self.github_oauth_token
        }

class Task():
    def __init__(self, name, completed, description, user_id):
        self.name = name
        self.completed = completed
        self.description = description
        self.user_id = user_id
    
    def serialize(self):
        return {
            'name': self.name,
            'completed': self.completed,
            'description': self.description,
            'user_id': self.user_id,
        }

class TodoList():
    def __init__(self, tasks_ids, id, user_id):
        self.tasks_ids = tasks_ids
        self.id = id
        self.user_id = user_id

    def serialize(self):
        return {
            'tasks': self.tasks_ids,
            'id': self.id,
            'user_id': self.user_id
        }