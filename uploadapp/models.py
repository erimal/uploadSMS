from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Smsimported(models.Model):
    other_id = models.CharField(max_length=50)
    mobilenumber = models.CharField('Mobile Number', max_length=20)
    message = models.CharField('Text Message', max_length=200)
    datecreated = models.DateField('Date Created')
    datesent = models.DateField('Date Sent')
    sent = models.IntegerField('Is SMS sent')
    attempt = models.IntegerField()
    provider = models.IntegerField('Telco')
    user_id = models.IntegerField('User ID')

    def __str__(self):
        return self.other_id

    # def datecreated(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.datecreated <= now

    # def sent(self):
    #     sent = 0
    #     return self.sent = sent

    def save_model(self, request, obj, form, change):
        obj.user_id = request.user
        print(request.user)
        return super(Smsimported, self).save_model(request, obj, form, change)