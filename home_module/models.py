import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse

import account_module.models


class Instructors(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام استاد')
    email = models.EmailField(max_length=50, verbose_name='ایمیل')
    phone = models.CharField(max_length=16, verbose_name='شماره تلفن')

    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'اساتید'

    def __str__(self):
        return self.name


class Prerequisite(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')

    class Meta:
        verbose_name = 'پیش نیاز'
        verbose_name_plural = 'پیش نیاز ها'

    def __str__(self):
        return self.title


class CourseHeadings(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    course = models.ForeignKey('Courses', db_index=True, on_delete=models.CASCADE, verbose_name='درس')

    class Meta:
        verbose_name = 'سر فصل'
        verbose_name_plural = 'سرفصل های دوره'

    def __str__(self):
        return self.course.title + '  -  ' + self.title


class CourseSessions(models.Model):
    course = models.ForeignKey('Courses', db_index=True, on_delete=models.CASCADE, verbose_name='دوره')
    course_heading = models.ForeignKey('CourseHeadings', db_index=True, on_delete=models.CASCADE,
                                       verbose_name='سر فصل')
    session = models.IntegerField(null=True, verbose_name='شماره جلسه', validators=[MinValueValidator(1)])
    title = models.CharField(max_length=100, db_index=True, verbose_name='عنوان')
    video_link_720p = models.URLField(max_length=200, verbose_name='لینک ویدیو 720 ', null=True)
    video_link_360p = models.URLField(max_length=200, verbose_name='لینک ویدیو 360 ', blank=True)
    description = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name = 'جلسه'
        verbose_name_plural = 'جلسات دوره ها'
        unique_together = ('course_heading', 'session')

    def __str__(self):
        return self.course.title + '  -  ' + self.course_heading.title + '  -  ' + self.title

    def save(self, *args, **kwargs):
        if self.video_link_360p == '':
            self.video_link_360p = self.video_link_720p
        super().save(*args, **kwargs)


class UserCourse(models.Model):
    user = models.ForeignKey(account_module.models.User, db_index=True, on_delete=models.CASCADE, verbose_name='کاربر')
    course = models.ForeignKey('Courses', db_index=True, on_delete=models.CASCADE, verbose_name='دوره')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='فعال باشد؟')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده؟')

    class Meta:
        verbose_name = 'دوره کاربر'
        verbose_name_plural = 'دوره های کاربر'
        unique_together = ('user', 'course',)

    def __str__(self):
        return self.user.username + '-' + self.course.title


class Courses(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='عنوان دوره')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='slug', blank=True)
    short_description = models.CharField(max_length=300, verbose_name='توضیحات کوتاه')
    description = models.CharField(max_length=200, verbose_name='توضیحات')
    instructor = models.ForeignKey('Instructors', on_delete=models.CASCADE, verbose_name='استاد دوره')
    main_picture = models.ImageField(upload_to='static/img/gallery', verbose_name='تصویر اصلی')
    second_picture = models.ImageField(upload_to='static/img/gallery', default=None, blank=True, null=True,
                                       verbose_name='تصویر دوم')
    price = models.IntegerField(db_index=True, verbose_name='قیمت دوره')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف دوره')
    duration = models.DurationField(verbose_name='مدت زمان دوره')
    prerequisites = models.ManyToManyField(Prerequisite, verbose_name='پیش نیاز' , blank=True,null=True)
    video_file = models.URLField(null=True, blank=True,
                                 verbose_name='لینک ویدیو پیش نمایش دوره', max_length=500)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5, 'حداکثر امتیاز 5 میاشد'), MinValueValidator(1, 'حداقل امتیاز 1 میباشد')],
        default=1, verbose_name='امتیاز')
    is_finished = models.BooleanField(default=False, verbose_name='تکمیل / درحال تکمیل')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن دوره')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده بودن دوره')
    is_in_slider = models.BooleanField(default=False, verbose_name='نمایش در اسلایدر')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', args=[self.slug])

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'




class HomePage(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_short_description = models.CharField(max_length=200, verbose_name='توضیحات کوتاه سایت', null=True, blank=True)
    site_description = models.CharField(max_length=200, verbose_name='توضیحات سایت', null=True, blank=True)
    site_headline_1 = models.CharField(max_length=200, verbose_name='سر 1 برگ سایت', null=True, blank=True)
    site_headline_2 = models.CharField(max_length=200, verbose_name='سر 2 برگ سایت', null=True, blank=True)
    site_headline_3 = models.CharField(max_length=200, verbose_name='سر 3 برگ سایت', null=True, blank=True)
    site_headline_4 = models.CharField(max_length=200, verbose_name='سر 4 برگ سایت', null=True, blank=True)
    site_headline_5 = models.CharField(max_length=200, verbose_name='سر 5 برگ سایت', null=True, blank=True)
    site_headline_6 = models.CharField(max_length=200, verbose_name='سر 6 برگ سایت', null=True, blank=True)
    site_home_image = models.ImageField(upload_to='static/img/gallery', verbose_name='تصویر صفحه اصلی', null=True,
                                        blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'صفحه اصلی'
        verbose_name_plural = 'صفحه اصلی'


class QuestionAndAnswer(models.Model):
    question = models.CharField(max_length=200,db_index=True, verbose_name='سوال')
    answer = models.CharField(max_length=200, verbose_name='پاسخ',null=True,blank=True)
    course = models.ForeignKey('Courses', on_delete=models.CASCADE,db_index=True, verbose_name='دوره')
    name = models.CharField(max_length=200, verbose_name='نام')
    is_approved = models.BooleanField(default=False,db_index=True, verbose_name='تایید شده')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'پرسش و پاسخ'
        verbose_name_plural = 'سوال و پاسخ'


@receiver(models.signals.post_delete, sender=HomePage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.site_home_image:
        if os.path.isfile(instance.site_home_image.path):
            os.remove(instance.site_home_image.path)



