from src.postgres.crud import Backend_Interface


if __name__ == "__main__":
    interfaces = Backend_Interface()
    interfaces.create_user_table()
    #interfaces.create_todo_table()
    #interfaces.create_task_table()
    interfaces.create_idea_table()
    interfaces.conn.close()

