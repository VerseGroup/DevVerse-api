class User():
    def __init__(self, username, email, password, phone, display_name, github_oauth_token, id):
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.display_name = display_name
        self.github_oauth_token = github_oauth_token
        self.id = id

    def serialize(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'display_name': self.display_name,
            'github_oauth_token': self.github_oauth_token,
            'id': self.id
        }

class Task():
    def __init__(self, name, completed, description, user_id, id):
        self.name = name
        self.completed = completed
        self.description = description
        self.user_id = user_id
        self.id = id
    
    def serialize(self):
        return {
            'name': self.name,
            'completed': self.completed,
            'description': self.description,
            'user_id': self.user_id,
            'id': self.id
        }

class TodoList():
    def __init__(self, tasks, id, user_id):
        self.tasks = tasks
        self.id = id
        self.user_id = user_id

    def serialize(self):
        return {
            'tasks': self.tasks,
            'id': self.id,
            'user_id': self.user_id
        }