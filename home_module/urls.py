from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='home_page'),
    path('courses/<slug:slug>', views.CourseDetailView.as_view(), name='course-detail'),
    path('payment/<slug:slug>', views.payment, name='payment'),
    path('courses', views.courses, name='courses'),
    path('tutorial-login/<slug:slug>', views.TutorialLoginView.as_view(), name='tutorial-login'),

]

handler404 = 'home_module.views.error_404'
handler500 = 'home_module.views.error_500'

