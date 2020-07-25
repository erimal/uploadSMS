from django.contrib import admin
from .models import Smsimported, Smsdelivered, File
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.urls import path
from uploadapp.myFile import SMSFile

class SmsimportedAdmin(admin.ModelAdmin):
    fields = ['other_id', 'mobilenumber', 'message']
    list_display = ('other_id', 'mobilenumber', 'message', 'datecreated')
    list_filter = ['datecreated']
    search_fields = ['mobilenumber']

    # return only the transaction of a particular user
    # And only SMS not sent
    def get_queryset(self, request):
        current_user = request.user
        qs = super(SmsimportedAdmin, self).get_queryset(request)
        return qs.filter(user_id=current_user.id, sent=0)

    def save_model(self, request, obj, form, change):
        current_user = request.user
        obj.datecreated = datetime.today()
        obj.datesent = datetime.today()
        obj.sent = 0
        obj.attempt = 0
        obj.provider = 2
        obj.user_id = current_user.id
        print(current_user.id)
        return super(SmsimportedAdmin, self).save_model(request, obj, form, change)

    # add action to the form
    def send_sms(modeladmin, request, queryset):
        #queryset.update(is_active=0)
        for i in queryset:
            print(i.mobilenumber)
        messages.success(request, "Selected Record(s) Marked as sent SMS Successfully !!")

    admin.site.add_action(send_sms, "Send SMS")

class SmsdeliveredAdmin(admin.ModelAdmin):
    fields = ['messageid', 'mobilenumber', 'message', 'datesubmitted']
    list_display = ('messageid', 'mobilenumber', 'message', 'datesubmitted')
    list_filter = ['datesubmitted']
    search_fields = ['mobilenumber']

    # return only the transaction of a particular user
    # And only SMS not sent
    def get_queryset(self, request):
        current_user = request.user
        qs = super(SmsdeliveredAdmin, self).get_queryset(request)
        return qs.filter(user_id=current_user.id)

    # add action to the archive the delivered SMS


class FileAdmin(admin.ModelAdmin):
    fields = ['description', 'document']
    list_display = ('description', 'document', 'datecreated')
    list_filter = ['datecreated']
    search_fields = ['description']

    # return only the transaction of a particular user
    def get_queryset(self, request):
        current_user = request.user
        qs = super(FileAdmin, self).get_queryset(request)
        return qs.filter(user_id=current_user.id)

    def save_model(self, request, obj, form, change):
        current_user = request.user
        obj.datecreated = datetime.today()
        obj.user_id = current_user.id
        filename = obj.document
        uploaded_file = request.FILES['document']
        print(uploaded_file)
        f = SMSFile()
        if f.upload(uploaded_file, obj.user_id):
            messages.success(request, "File uploaded Successfully !")
            return super(FileAdmin, self).save_model(request, obj, form, change)
        else:
            messages.success(request, 'File can not be uploaded twice. Contact Admin !')
            return False  #super(FileAdmin, self)

admin.site.register(File, FileAdmin)
admin.site.register(Smsimported, SmsimportedAdmin)
admin.site.register(Smsdelivered, SmsdeliveredAdmin)


