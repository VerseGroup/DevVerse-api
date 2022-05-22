from typing import Dict
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
        
    
    def create_task_table(self):
        """
        This function creates a table in the database called tasks.
        """
        create_task_table_query = """
        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(500) NOT NULL,
            completed BOOLEAN NOT NULL,
            description VARCHAR(500) NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(create_task_table_query)
        self.conn.commit()
        cursor.close()
        
        
    def create_todo_table(self):
        """
        This function creates a table in the database called todos.
        """
        create_todo_table_query = """
        CREATE TABLE todos (
            id SERIAL PRIMARY KEY,
            tasks_ids INTEGER [] NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(create_todo_table_query)
        self.conn.commit()
        cursor.close()
        

    def create_user(self, user: User):
        try:
            insert_user_query = """
            INSERT INTO users (username, email, phone, name, github_oauth_token)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor = self.conn.cursor()
            cursor.execute(insert_user_query, (user.username, user.email, user.phone, user.name, user.github_oauth_token))
            self.conn.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    def create_task(self, task: Task):
        try:
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
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    def create_todo_list(self, todo_list: TodoList):
        try:
            """
            This function creates a todo list in the database.
            """
            create_todo_list_query = """
            INSERT INTO todos (tasks_ids, user_id)
            VALUES (%s, %s);
            """
            cursor = self.conn.cursor()
            cursor.execute(create_todo_list_query, (todo_list.tasks_ids, todo_list.user_id,))
            self.conn.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            return error

    def update_user(self, user: User, id: int):
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

    def update_task(self, task: Task):
        """
        This function updates a task in the database.
        """
        update_task_query = """
        UPDATE tasks
        SET name = %s, completed = %s, description = %s, user_id = %s
        WHERE id = %s;
        """
        cursor = self.conn.cursor()
        cursor.execute(update_task_query, (task.name, task.completed, task.description, task.user_id, task.id,))
        self.conn.commit()
        cursor.close()

    def update_todo_list(self, todo_list: TodoList):
        """
        This function updates a todo list in the database.
        """
        update_todo_list_query = """
        UPDATE todos
        SET tasks_ids = %s
        WHERE user_id = %s;
        """
        cursor = self.conn.cursor()
        cursor.execute(update_todo_list_query, (todo_list.tasks_ids, todo_list.user_id, todo_list.id))
        self.conn.commit()
        cursor.close()

    def fetch_user_by_oauth(self, oauth_token: str):
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

        # if user exists return user esle return None
        if user == None:
            return None
        return user[0]

    def fetch_todo_list_by_user_id(self, user_id: int):
        """
        This function fetches a todo list by user id from the database.
        """
        fetch_todo_list_by_user_id_query = """
        SELECT * FROM todos WHERE user_id = %s;
        """
        cursor = self.conn.cursor()
        cursor.execute(fetch_todo_list_by_user_id_query, (user_id,))
        todo_list = cursor.fetchone()
        cursor.close()
        if todo_list == None:
            return None
        return todo_list[0]

    def fetch_task_by_todo_list_id(self, todo_list_ids: list):
        """
        This function fetches a task by todo list id from the database.
        """
        fetch_task_by_todo_list_id_query = f"""
        SELECT * FROM tasks WHERE id = %s {"OR id = %s " * (len(todo_list_ids) - 1)};
        """
        cursor = self.conn.cursor()
        cursor.execute(fetch_task_by_todo_list_id_query, tuple(todo_list_ids))
        tasks = cursor.fetchall()
        cursor.close()
        return [Task(*task).serialize() for task in tasks]
    