from src.postgres.models import *
from dotenv import load_dotenv
import psycopg2
import os




load_dotenv()

class Backend_Interface:
    def __init__(self):
        self.DATABASE_URL = os.environ['DATABASE_URL']
        try:
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"\nFailed: unable to connect to database with error \"{error}\"")
            return None

    def create_user_table(self):
        self.__init__()
        """
        This function creates a table in the database called users.
        """
        create_user_table_query = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(500) NOT NULL,
            email VARCHAR(500) NOT NULL,
            phone VARCHAR(500) NOT NULL,
            name VARCHAR(500) NOT NULL,
            github_oauth_token VARCHAR(500) NOT NULL
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(create_user_table_query)
        self.conn.commit()
        cursor.close()
        self.conn.close()
        
    def create_todo_table(self):
        self.__init__()
        """
        This function creates a table in the database called todos.
        """
        create_todo_table_query = """
        CREATE TABLE todos (
            id SERIAL PRIMARY KEY,
            tasks_ids INTEGER [] NOT NULL,
            name VARCHAR(500) NOT NULL,
            description VARCHAR(500) NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(create_todo_table_query)
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def create_user(self, user: User):
        try:
            self.__init__()
            insert_user_query = """
            INSERT INTO users (username, email, phone, name, github_oauth_token)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor = self.conn.cursor()
            cursor.execute(insert_user_query, (user.username, user.email, user.phone, user.name, user.github_oauth_token))
            self.conn.commit()
            cursor.close()
            self.conn.close()
            self.__init__()

            # fetching the user id
            """
            This function fetches a user id by oauth token from the database.
            """
            fetch_user_id_by_oauth_query = """
            SELECT id FROM users WHERE github_oauth_token = %s LIMIT 1;
            """
            cursor = self.conn.cursor()
            cursor.execute(fetch_user_id_by_oauth_query, (user.github_oauth_token,))
            user_id = cursor.fetchone()
            cursor.close()
            self.conn.close()
            return user_id[0]
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    def create_task(self, task: Task):
        try:
            self.__init__()
            """
            This function creates a task in the database.
            """
            create_task_query = """
            INSERT INTO tasks (name, completed, description, user_id)
            VALUES (%s, %s, %s, %s);
            """
            cursor = self.conn.cursor()
            cursor.execute(create_task_query, (task.name, task.completed, task.description, task.user_id,))
            self.conn.commit()
            cursor.close()
            self.conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    def create_todo_list(self, todo_list: TodoList):
        try:
            self.__init__()
            """
            This function creates a todo list in the database.
            """
            create_todo_list_query = """
            INSERT INTO todos (tasks_ids, user_id, name, description)
            VALUES (%s, %s, %s, %s);
            """
            cursor = self.conn.cursor()
            cursor.execute(create_todo_list_query, (todo_list.tasks_ids, todo_list.user_id, todo_list.name, todo_list.description,))
            self.conn.commit()
            cursor.close()
            self.conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    def update_user(self, user: User, id: int):
        self.__init__()
        """
        This function updates a user in the database.
        """
        update_user_query = """
        UPDATE users
        SET username = %s, email = %s, phone = %s, name = %s, github_oauth_token = %s
        WHERE id = %s;
        """
        cursor = self.conn.cursor()
        cursor.execute(update_user_query, (user.username, user.email, user.phone, user.name, user.github_oauth_token, id,))
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def update_task(self, task: Task, task_id):
        self.__init__()
        """
        This function updates a task in the database.
        """
        update_task_query = """
        UPDATE tasks
        SET name = %s, completed = %s, description = %s, user_id = %s, todo_list_id = %s,
        WHERE id = %s;
        """
        cursor = self.conn.cursor()
        cursor.execute(update_task_query, (task.name, task.completed, task.description, task.user_id, task.todo_list_id, task_id,))
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def update_todo_list(self, todo_list: TodoList):
        self.__init__()
        """
        This function updates a todo list in the database.
        """
        update_todo_list_query = """
        UPDATE todos
        SET tasks_ids = %s, user_id = %s, name = %s, description = %s
        WHERE id = %s;
        """
        cursor = self.conn.cursor()
        cursor.execute(update_todo_list_query, (todo_list.tasks_ids, todo_list.user_id, todo_list.name, todo_list.description, todo_list.id,))
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def fetch_user_by_oauth(self, oauth_token: str):
        self.__init__()
        """
        This function fetches a user by oauth token.
        """
        fetch_user_by_oauth_query = """
        SELECT * FROM users WHERE github_oauth_token = %s LIMIT 1;
        """
        cursor = self.conn.cursor()
        cursor.execute(fetch_user_by_oauth_query, (oauth_token,))
        user = cursor.fetchone()
        cursor.close()
        self.conn.close()

        # if user exists return user esle return None
        if user == None:
            return None
        return user

    def fetch_user_id_by_oauth(self, oauth_token: str):
        self.__init__()
        """
        This function fetches a user id by oauth token.
        """
        fetch_user_id_by_oauth_query = """
        SELECT id FROM users WHERE github_oauth_token = %s LIMIT 1;
        """
        cursor = self.conn.cursor()
        cursor.execute(fetch_user_id_by_oauth_query, (oauth_token,))
        user_id = cursor.fetchone()
        cursor.close()
        self.conn.close()
        return user_id[0]
        

    def fetch_todo_lists_by_oauth(self, oauth_token: str):
        # convert oauth token to user id
        self.__init__()
        user_id = self.fetch_user_by_oauth(oauth_token)

        # fetch todo lists by user id
        self.__init__()
        """
        This function fetches a todo list by oauth from the database.
        """
        fetch_todo_list_by_user_id_query = """
        SELECT * FROM todos WHERE user_id = %s;
        """
        cursor = self.conn.cursor()
        cursor.execute(fetch_todo_list_by_user_id_query, (user_id,))
        todo_list = cursor.fetchall()
        cursor.close()
        self.conn.close()
        if todo_list == None:
            return None
        todo_list = list(todo_list)

        todo_list = [{"id": x[0], "task_ids": x[1], "user_id": x[2]} for x in todo_list]
        return todo_list 

    def fetch_tasks_by_todo_list_id(self, todo_list_id: int):
        self.__init__()
        """
        This function fetches a task by todo list id from the database.
        """
        fetch_task_by_todo_list_id_query = """
        SELECT * FROM tasks WHERE id = %s;
        """
        cursor = self.conn.cursor()
        cursor.execute(fetch_task_by_todo_list_id_query, (todo_list_id,))
        tasks = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return [{"id": task[0], "name": task[1], "completed": task[2], "description": task[3], "user_id": task[4]} for task in tasks]

    def fetch_user_by_username(self, username: str):
        self.__init__()
        """
        This function fetches a user by username from the database.
        """
        fetch_user_by_username_query = """
        SELECT * FROM users WHERE username = %s LIMIT 1;
        """
        cursor = self.conn.cursor()
        cursor.execute(fetch_user_by_username_query, (username,))
        user = cursor.fetchone()
        cursor.close()
        self.conn.close()
        if user == None:
            return None
        return list(user)
    
    
