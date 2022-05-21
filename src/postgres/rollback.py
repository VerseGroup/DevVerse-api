from dotenv import load_dotenv
import psycopg2
import os



load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

curs = conn.cursor()
curs.execute("ROLLBACK")
conn.commit()
