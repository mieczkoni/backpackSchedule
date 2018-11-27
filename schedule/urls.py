from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.admin_users, name='users'),
    path('subjects', views.admin_subjects, name='subjects'),
    path('subject_ratings', views.admin_subject_ratings, name='subject_ratings'),
    path('save_ratings', views.save_ratings, name='save_ratings')
]
