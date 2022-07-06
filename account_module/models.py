import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=16, verbose_name='شماره تلفن')
    otp = models.CharField(max_length=6, verbose_name='کد امنیتی', blank=True, null=True)
    otp_expire_time = models.DateTimeField(verbose_name='زمان انقضای کد امنیتی', blank=True, null=True,)
    otp_sent_block_time = models.DateTimeField(verbose_name='زمان بلاک کردن ارسال کد امنیتی', blank=True, null=True)


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username
