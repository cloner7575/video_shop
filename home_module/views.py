from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import QuestionAndAnswerForm
from .models import Courses, CourseHeadings, CourseSessions, UserCourse, HomePage, QuestionAndAnswer
from gallery_module.models import Gallery


# Create your views here.

def index_page(request):
    courses = Courses.objects.all()
    home_page = HomePage.objects.first()
    context = {
        'courses': courses,
        'home_page': home_page
    }
    return render(request, 'home_module/index_page.html', context=context)


def footer_context(request):
    gallery_footer = Gallery.objects.filter(is_active=True)
    return {
        'gallery_footer': gallery_footer
    }


def header_context(request):
    home_page = HomePage.objects.first()
    return {
        'home_page': home_page
    }


def error_404(request, exception):
    return render(request, '404.html')

def error_500(request):
    return render(request, '500.html')

def courses(request):
    courses = Courses.objects.all()
    new_courses = []
    for course in courses:
        course_dict = {
            'main_picture': course.main_picture,
            'discount': course.discount,
            'title': course.title,
            'price': course.price,
            'slug': course.slug,
            'rate_range': range(course.rating),
            'short_description': course.short_description,
            'instructor': course.instructor,
            'duration': course.duration,

        }
        new_courses.append(course_dict)

    context = {
        'courses': new_courses
    }
    return render(request, 'home_module/courses_page.html', context=context)


class TutorialLoginView(View):
    def get(self, request, slug):
        course = Courses.objects.get(slug=slug)
        course_session = CourseSessions.objects.filter(course=course)
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        course_heading = CourseHeadings.objects.filter(course=course)
        question_and_answer = QuestionAndAnswer.objects.filter(course=course)
        question_form = QuestionAndAnswerForm()
        if course.discount:
            total_price = course.price - course.discount
        else:
            total_price = course.price

        context = {
            'total_price': total_price,
            'course_heading': course_heading,
            'course': course,
            'course_session': course_session,
            'user_course': user_course,
            'question_form': question_form,
            'question_and_answer': question_and_answer
        }
        return render(request, 'home_module/tutorial_login.html', context=context)

    def post(self, request, slug):
        question_form = QuestionAndAnswerForm(request.POST)
        course = Courses.objects.get(slug=slug)

        if question_form.is_valid():
            question_and_answer = QuestionAndAnswer(question=question_form.cleaned_data.get('question'),
                                                    name=question_form.cleaned_data.get('name'),
                                                    course=course,
                                                    )

            question_and_answer.save()
            return redirect(reverse('course-detail', args=[slug]))
        else:
            context = {
                'course': course,
                'question_form': question_form
            }
            return render(request, 'home_module/tutorial.html', context=context)



class CourseDetailView(View):
    def get(self, request, slug):
        course = Courses.objects.get(slug=slug)
        course_heading = CourseHeadings.objects.filter(course=course)
        question_and_answer = QuestionAndAnswer.objects.filter(course=course)
        question_form = QuestionAndAnswerForm()
        if course.discount:
            total_price = course.price - course.discount
        else:
            total_price = course.price

        context = {
            'total_price': total_price,
            'course_heading': course_heading,
            'course': course,
            'question_and_answer': question_and_answer,
            'question_form': question_form
        }
        return render(request, 'home_module/tutorial.html', context=context)

    def post(self, request, slug):
        question_form = QuestionAndAnswerForm(request.POST)
        course = Courses.objects.get(slug=slug)


        if question_form.is_valid():
            question_and_answer = QuestionAndAnswer(question=question_form.cleaned_data.get('question'),
                                                    name=question_form.cleaned_data.get('name'),
                                                    course=course,
                                                    )

            question_and_answer.save()
            return redirect(reverse('course-detail',args=[slug]))
        else:
            context = {
                'course': course,
                'question_form': question_form
            }
            return render(request, 'home_module/tutorial.html', context=context)

def payment(request, slug):
    course = Courses.objects.get(slug=slug)
    user_course = UserCourse.objects.filter(user=request.user, course=course)
    if not user_course:
        new_user_course = UserCourse(user=request.user, course=course, is_active=False)
        new_user_course.save()
    context = {
        'course': course
    }
    return render(request, 'home_module/payment.html', context=context)


