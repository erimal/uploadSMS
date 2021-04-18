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

class dbSMS:

    def add_sms(r, user_id):
        datecreated = datetime.today()
        SQL_i = "insert into uploadapp_smsimported (other_id,	mobilenumber, message,datecreated,sent,attempt,provider,user_id) " \
                f"values('{r['id']}', '{r['phone']}', '{r['text']}', '{datecreated}','0','0', '2','{user_id}')"
        print("SQL to insert: " + SQL_i)
        cursor.execute(SQL_i)
        conn.commit()
#--end of the class

    def deliver_message(r,resource_id,user_id):
        date_sent = datetime.today() #.strftime('%Y-%m-%d')

        # update the import table
        SQL_u = f"update uploadapp_smsimported set datesent='{date_sent}', sent = 1 , attempt = 1 where other_id='{r['id']}'"
        cursor.execute(SQL_u)
        conn.commit()

        #insert into the SMSDelivery date
        SQL_i = "insert into uploadapp_smsdelivered (smsimported_id, messageId, mobilenumber,message, datesubmitted, provider,delivered,user_id) " \
              f"values('{r['id']}', '{resource_id}', '{r['mobilenumber']}', '{r['message']}', '{date_sent}', '2','0','{user_id}')"
        #print("SQL to insert: " + SQL_i)
        cursor.execute(SQL_i)
        conn.commit()


def add_sms(r):
    datecreated = datetime.today().strftime('%Y-%m-%d')

    SQL_i = "insert into uploadapp_smsimported (other_id,	mobilenumber, message,datecreated,sent,attempt,provider,user_id) " \
            f"values('{r['id']}', '{r['mobilenumber']}', '{r['message']}', '{datecreated}','0','0', '2','1')"

    print("SQL to insert in add_sms: " + SQL_i)
    cursor.execute(SQL_i)
    conn.commit()