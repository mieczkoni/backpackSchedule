from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save_ratings', views.save_ratings, name='save_ratings')
]
