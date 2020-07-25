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

def add_sms(r, user_id):
    datecreated = datetime.today()
    SQL_i = "insert into uploadapp_smsimported (other_id,	mobilenumber, message,datecreated,sent,attempt,provider,user_id) " \
            f"values('{r['id']}', '{r['phone']}', '{r['text']}', '{datecreated}','0','0', '2','{user_id}')"
    print("SQL to insert: " + SQL_i)
    cursor.execute(SQL_i)
    conn.commit()