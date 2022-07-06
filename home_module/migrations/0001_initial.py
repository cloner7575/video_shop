# Generated by Django 4.0.4 on 2022-06-05 07:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=200, verbose_name='نام سایت')),
                ('site_short_description', models.CharField(blank=True, max_length=200, null=True, verbose_name='توضیحات کوتاه سایت')),
                ('site_description', models.CharField(blank=True, max_length=200, null=True, verbose_name='توضیحات سایت')),
                ('site_headline_1', models.CharField(blank=True, max_length=200, null=True, verbose_name='سر 1 برگ سایت')),
                ('site_headline_2', models.CharField(blank=True, max_length=200, null=True, verbose_name='سر 2 برگ سایت')),
                ('site_headline_3', models.CharField(blank=True, max_length=200, null=True, verbose_name='سر 3 برگ سایت')),
                ('site_headline_4', models.CharField(blank=True, max_length=200, null=True, verbose_name='سر 4 برگ سایت')),
                ('site_headline_5', models.CharField(blank=True, max_length=200, null=True, verbose_name='سر 5 برگ سایت')),
                ('site_headline_6', models.CharField(blank=True, max_length=200, null=True, verbose_name='سر 6 برگ سایت')),
                ('site_home_image', models.ImageField(blank=True, null=True, upload_to='static/img/gallery', verbose_name='تصویر صفحه اصلی')),
            ],
            options={
                'verbose_name': 'صفحه اصلی',
                'verbose_name_plural': 'صفحه اصلی',
            },
        ),
        migrations.CreateModel(
            name='Instructors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام استاد')),
                ('email', models.EmailField(max_length=50, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=16, verbose_name='شماره تلفن')),
            ],
            options={
                'verbose_name': 'استاد',
                'verbose_name_plural': 'اساتید',
            },
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'پیش نیاز',
                'verbose_name_plural': 'پیش نیاز ها',
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='عنوان دوره')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='slug')),
                ('short_description', models.CharField(max_length=300, verbose_name='توضیحات کوتاه')),
                ('description', models.CharField(max_length=200, verbose_name='توضیحات')),
                ('main_picture', models.ImageField(upload_to='static/img/gallery', verbose_name='تصویر اصلی')),
                ('second_picture', models.ImageField(blank=True, default=None, null=True, upload_to='static/img/gallery', verbose_name='تصویر دوم')),
                ('price', models.IntegerField(db_index=True, verbose_name='قیمت دوره')),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='تخفیف دوره')),
                ('duration', models.DurationField(verbose_name='مدت زمان دوره')),
                ('video_file', models.URLField(blank=True, max_length=500, null=True, verbose_name='لینک ویدیو پیش نمایش دوره')),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5, 'حداکثر امتیاز 5 میاشد'), django.core.validators.MinValueValidator(1, 'حداقل امتیاز 1 میباشد')], verbose_name='امتیاز')),
                ('is_finished', models.BooleanField(default=False, verbose_name='تکمیل / درحال تکمیل')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال بودن دوره')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='حذف شده بودن دوره')),
                ('is_in_slider', models.BooleanField(default=False, verbose_name='نمایش در اسلایدر')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home_module.instructors', verbose_name='استاد دوره')),
                ('prerequisites', models.ManyToManyField(to='home_module.prerequisite', verbose_name='پیش نیاز')),
            ],
            options={
                'verbose_name': 'دوره',
                'verbose_name_plural': 'دوره ها',
            },
        ),
        migrations.CreateModel(
            name='CourseHeadings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home_module.courses', verbose_name='درس')),
            ],
            options={
                'verbose_name': 'سر فصل',
                'verbose_name_plural': 'سرفصل های دوره',
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='فعال باشد؟')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='حذف شده؟')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home_module.courses', verbose_name='دوره')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'دوره کاربر',
                'verbose_name_plural': 'دوره های کاربر',
                'unique_together': {('user', 'course')},
            },
        ),
        migrations.CreateModel(
            name='CourseSessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='شماره جلسه')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='عنوان')),
                ('video_link_720p', models.URLField(null=True, verbose_name='لینک ویدیو 720 ')),
                ('video_link_360p', models.URLField(blank=True, verbose_name='لینک ویدیو 360 ')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home_module.courses', verbose_name='دوره')),
                ('course_heading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home_module.courseheadings', verbose_name='سر فصل')),
            ],
            options={
                'verbose_name': 'جلسه',
                'verbose_name_plural': 'جلسات دوره ها',
                'unique_together': {('course_heading', 'session')},
            },
        ),
    ]
