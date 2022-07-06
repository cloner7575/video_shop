# Generated by Django 4.0.4 on 2022-07-05 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallery_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='owner',
            field=models.CharField(default='ناشناس', max_length=200, verbose_name='نام صاحب اثر'),
        ),
        migrations.CreateModel(
            name='UserArtwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(default=False, verbose_name='آیا سفارش داده شده است؟')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_received', models.BooleanField(default=False, verbose_name='آیا دریافت شده است؟')),
                ('date_sent', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ ارسال')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery_module.gallery')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'خرید نقاشی برای کاربر',
                'verbose_name_plural': 'خرید نقاشی های کاربران',
            },
        ),
    ]