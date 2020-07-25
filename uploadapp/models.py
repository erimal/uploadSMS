from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.

class Smsimported(models.Model):
    other_id = models.CharField(max_length=50)
    mobilenumber = models.CharField('Mobile Number', max_length=20)
    message = models.CharField('Text Message', max_length=200)
    datecreated = models.DateTimeField('Date Created')
    datesent = models.DateTimeField('Date Sent')
    sent = models.IntegerField('Is SMS sent')
    attempt = models.IntegerField()
    provider = models.IntegerField('Telco')
    user_id = models.IntegerField('User ID')

    def __str__(self):
        return self.other_id

    def save_model(self, request, obj, form, change):
        obj.user_id = request.user
        print(request.user)
        return super(Smsimported, self).save_model(request, obj, form, change)

    # change name of the model
    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = 'SMS'

# delivered SMS model
class Smsdelivered(models.Model):
    smsimported_id = models.IntegerField('SMS ID')
    messageid = models.CharField('Message ID', max_length=200)
    mobilenumber = models.CharField('Mobile Number', max_length=20)
    message = models.CharField('Text Message', max_length=200)
    datesubmitted = models.DateTimeField('Date submitted')
    datedelivered = models.DateTimeField('Date Delivered',null=True, blank=True)
    delivered = models.IntegerField('Is SMS delivered')
    msgstatus = models.CharField('Message Status', max_length=50, null=True, blank=True)
    provider = models.IntegerField('Telco')
    user_id = models.IntegerField('User ID')

    def __str__(self):
        return self.messageid

    # change name of the model
    class Meta:
        verbose_name = 'SMS Delivered'
        verbose_name_plural = 'SMS Delivered'

# upload document
class File(models.Model):
    description = models.CharField(max_length=255)
    document = models.FileField(upload_to='media/')
    datecreated = models.DateTimeField('Date Created')
    user_id = models.IntegerField('User ID')

    def __str__(self):
        return self.description