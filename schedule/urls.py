from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.admin_users, name='users'),
    path('subjects', views.admin_subjects, name='subjects'),
    path('subject_ratings', views.admin_subject_ratings, name='subject_ratings'),
    path('solver', views.solver_site, name='solver'),
    path(r'^show_subject/(?P<parameter>)/$', views.show_subject, name='show_subject'),
    path(r'^show_user/(?P<parameter>)/$', views.show_user, name='show_user'),
    path('save_ratings', views.save_ratings, name='save_ratings'),
    path('solve_problem', views.solve_problem, name='solve_problem'),
    path('random_objects', views.random_objects, name='random_objects')
]
