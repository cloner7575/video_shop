from django.urls import path
from gallery_module import views
urlpatterns = [
    path('', views.index, name='gallery_index'),
    path('/<int:pk>/', views.gallery_detail, name='gallery_detail'),
    path('/<int:pk>/payment/', views.gallery_payment, name='gallery_payment'),

]