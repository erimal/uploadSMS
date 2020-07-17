from django.shortcuts import render
import csv
import pandas as pd
import os
import uploadapp.dbConfig as db

# Create your views here.

from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


def upload(request):
        context = {}

        try:

            if request.method == 'POST' and request.FILES['document']:
                uploaded_file = request.FILES['document']
                name = ''
                print(uploaded_file.name)
                if os.path.isfile(f'media/{uploaded_file.name}'):
                    # if exist then do not save the file again
                    print("found")
                    context['url'] = 'File can not be uploaded twice. Contact Admin'
                else:
                    # if not in the folder write to file
                    fs = FileSystemStorage()
                    name = fs.save(uploaded_file.name, uploaded_file)
                    context['url'] = fs.url(name)
                    print("not found")

                    # upload the file in the DB
                    if uploaded_file:
                        print("ready to upload ")
                        df = pd.read_csv(f'media/{uploaded_file.name}')
                        print(df)
                        for index, row in df.iterrows():
                            id = row['id']
                            phone = row['phone']
                            msg = row['text']
                            #print(id)
                            #db.add_sms(row)
        except:
            print("there is an error ")

        return render(request, "uploadapp/upload.html", context)