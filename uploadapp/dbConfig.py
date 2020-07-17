import mysql.connector
import uploadapp.dbSettings as db
from datetime import datetime
import pandas as pd

# connect to DB
conn = mysql.connector.connect(
  host=db.DB_SERVER,
  user=db.DB_USERNAME,
  password=db.DB_PASSWORD,
  database=db.DB_DATABASE
)
cursor = conn.cursor()

def add_sms(r):
    datecreated = datetime.today().strftime('%Y-%m-%d')
    SQL_i = "insert into smsimported (other_id,	mobilenumber, message,datecreated,sent,attempt,provider) " \
            f"values('{r['id']}', '{r['phone']}', '{r['text']}', '{datecreated}','0','0', '2')"
    # print("SQL to insert: " + SQL_i)
    cursor.execute(SQL_i)
    conn.commit()