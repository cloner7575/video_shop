# Generated by Django 4.0.4 on 2022-06-05 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, null=True, to='home_module.prerequisite', verbose_name='پیش نیاز'),
        ),
    ]