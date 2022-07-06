from django.contrib import admin
from . import models


# Register your models here.

class HomePageAdmin(admin.ModelAdmin):
    list_display = ['id', 'site_name', 'site_short_description', 'site_description',
                    'site_headline_1',
                    'site_headline_2',
                    'site_headline_3',
                    'site_headline_4',
                    'site_headline_5',
                    'site_headline_6',
                    'site_home_image'
                    ]

    list_display_links = ['id']
    list_editable = ['site_name', 'site_short_description', 'site_description',
                     'site_headline_1',
                     'site_headline_2',
                     'site_headline_3',
                     'site_headline_4',
                     'site_headline_5',
                     'site_headline_6',
                     'site_home_image'

                     ]


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'is_active', ]
    list_editable = ['user', 'course', 'is_active', ]
    search_fields = ['user__username']


admin.site.register(models.HomePage, HomePageAdmin)

admin.site.register(models.Courses, CourseAdmin)
admin.site.register(models.Instructors)
admin.site.register(models.Prerequisite)
admin.site.register(models.CourseHeadings)
admin.site.register(models.UserCourse, UserCourseAdmin)
admin.site.register(models.CourseSessions)
admin.site.register(models.QuestionAndAnswer)
