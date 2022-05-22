from code import interact
import os
import psycopg2
from crud import Backend_Interface

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

interfaces = Backend_Interface()
interfaces.create_user_table()
interfaces.create_todo_table()
interfaces.create_task_table()
interfaces.conn.close()

