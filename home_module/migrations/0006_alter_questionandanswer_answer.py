# Generated by Django 4.0.4 on 2022-06-20 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_module', '0005_questionandanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionandanswer',
            name='answer',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='پاسخ'),
        ),
    ]
