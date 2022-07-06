import os

from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class Gallery(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    image = models.ImageField(upload_to='static/img/gallery/', verbose_name='تصویر')
    material = models.CharField(max_length=200, verbose_name='متریال', default='سیاه قلم')
    size = models.CharField(max_length=200, verbose_name='سایز', default='30*40')
    owner = models.CharField(max_length=200, verbose_name='نام صاحب اثر', default='ناشناس')
    price = models.IntegerField(verbose_name='قیمت', default=0)
    discount = models.IntegerField(verbose_name='تخفیف', default=0)
    description = models.TextField(verbose_name='توضیحات', default='')
    second_image = models.ImageField(upload_to='static/img/gallery/', verbose_name='تصویر دوم', null=True, blank=True)
    third_image = models.ImageField(upload_to='static/img/gallery/', verbose_name='تصویر سوم', null=True, blank=True)
    fourth_image = models.ImageField(upload_to='static/img/gallery/', verbose_name='تصویر چهارم', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='نمایش در زیر صفحه ')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    class Meta:
        verbose_name = 'عکس'
        verbose_name_plural = 'گالری'


class UserArtwork(models.Model):
    user = models.ForeignKey('account_module.User', on_delete=models.CASCADE)
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False, verbose_name='آیا سفارش داده شده است؟')
    date = models.DateTimeField(auto_now_add=True)
    is_received = models.BooleanField(default=False, verbose_name='آیا دریافت شده است؟')
    date_sent = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ ارسال')

    def __str__(self):
        return self.user.username + ' - ' + self.gallery.title

    class Meta:
        verbose_name = 'خرید نقاشی برای کاربر'
        verbose_name_plural = 'خرید نقاشی های کاربران'


@receiver(models.signals.post_delete, sender=Gallery)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
