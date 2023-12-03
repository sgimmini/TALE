from django.urls import path
from . import views

urlpatterns = [
    path('', views.front_page, name='front_page'),
    path('calculation/', views.calculation_view, name='calculation'),
    path('upload_file/', views.upload_file_view, name='upload_file')
]
