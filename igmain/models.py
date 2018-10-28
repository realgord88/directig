from django.db import models
from django.contrib.auth.models import User

class IGaccount(models.Model):
    igaccount = models.CharField(max_length=30, help_text="account")
    igpassword = models.CharField(max_length=30, help_text="password")

    class Meta:
        verbose_name = 'account for direct'
        verbose_name_plural = 'account for direct'


class IGmodel(models.Model):
    igmodel = models.CharField(max_length=30, help_text="model account")
    msg_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'model account'
        verbose_name_plural = 'model account'

class IGpublic(models.Model):
    igpublic = models.CharField(max_length=30, help_text="public account")

    class Meta:
        verbose_name = 'public'
        verbose_name_plural = 'public'