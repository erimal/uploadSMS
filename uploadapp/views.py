from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import csv
import pandas as pd
import os
from .dbConfig import dbSMS as db
from .utils import Orange as ut
#import uploadSMS.uploadapp.dbConfig as db
#import uploadSMS.uploadapp.utils as ut

from django.contrib import messages

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage

@login_required
def upload(request):
        context = {}

        try:

            if request.method == 'POST' and request.FILES['document']:
                user = request.POST.get('id')
                current_user = request.user.id
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
                            db.add_sms(row, current_user)
        except Exception as e:
            print(e)

        return render(request, "uploadapp/upload.html", context)

@login_required
def sendtest(request):

    if request.method == 'POST':
        phone = request.POST.get('phone')
        current_user = request.user.id

        if len(phone) == 12:
            print("phone is ok")
            ## Validation ok send sms
            #messages.success(request, 'A test SMS was sent successfully to number.')
            resp = "A test SMS was sent successfully to number."
            #ut.get_orange_token()
            ut.send_SMS(phone, current_user)
            redirect('sendtest')
        else:
            #messages.warning(request, 'Phone number should be 12 digits.')
            resp = "Phone number should be 12 digits."
            print("phone is less than 12 digist")
            redirect('sendtest')

        #return JsonResponse(resp, safe=False)

    return render(request, "uploadapp/sendtest.html")
