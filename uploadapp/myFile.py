import csv
import pandas as pd
import os
import uploadapp.dbConfig as db

# Create your views here.


from django.core.files.storage import FileSystemStorage

class SMSFile:

    def upload(self, file, user_id):
            ret = False

            try:
                 if os.path.isfile(f'media/{file.name}'):
                    # if exist then do not save the file again
                    print("found")
                 else:
                    print("not found")
                    # if not in the folder write to file
                    fs = FileSystemStorage()
                    name = fs.save(file.name, file)
                    # upload the file in the DB
                    if file:
                        print("ready to upload ")
                        df = pd.read_csv(f'media/{file.name}')
                        print(df)
                        for index, row in df.iterrows():
                            id = row['id']
                            phone = row['phone']
                            msg = row['text']
                            #print(id)
                            db.add_sms(row, user_id)
                    ret = True
            except:
                print("there is an error ")

            return ret
