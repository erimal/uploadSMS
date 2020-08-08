import mysql.connector
from datetime import datetime
from django.conf import settings as DB

# connect to DB
conn = mysql.connector.connect(
  host=DB.DATABASES['default']['HOST'],
  user=DB.DATABASES['default']['USER'],
  password=DB.DATABASES['default']['PASSWORD'],
  database=DB.DATABASES['default']['NAME']
)
cursor = conn.cursor()


def add_sms(r, user_id):
    datecreated = datetime.today()
    SQL_i = "insert into uploadapp_smsimported (other_id,	mobilenumber, message,datecreated,sent,attempt,provider,user_id) " \
            f"values('{r['id']}', '{r['phone']}', '{r['text']}', '{datecreated}','0','0', '2','{user_id}')"
    print("SQL to insert: " + SQL_i)
    cursor.execute(SQL_i)
    conn.commit()