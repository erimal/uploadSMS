from django.contrib import admin
from .models import Smsimported
from datetime import datetime

# Register your models here.


class SmsimportedAdmin(admin.ModelAdmin):
    fields = ['other_id', 'mobilenumber', 'message']
    list_display = ('other_id', 'mobilenumber', 'message', 'datecreated')
    list_filter = ['datecreated']
    search_fields = ['mobilenumber']

    def save_model(self, request, obj, form, change):
        current_user = request.user
        obj.datecreated = datetime.today().strftime('%Y-%m-%d')
        obj.datesent = datetime.today().strftime('%Y-%m-%d')
        obj.sent = 0
        obj.attempt = 0
        obj.provider = 2
        obj.user_id = current_user.id
        print(current_user.id)
        return super(SmsimportedAdmin, self).save_model(request, obj, form, change)

admin.site.register(Smsimported, SmsimportedAdmin)


