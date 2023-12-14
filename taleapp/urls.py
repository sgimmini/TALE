from django.urls import path
from . import views

urlpatterns = [
    path('', views.front_page, name='front_page'),
    path('calculation/', views.calculation_view, name='calculation'),
    path('upload_file/', views.upload_file_view, name='upload_file'),
    path('download_selected/', views.download_selected_files, name='download_selected_files'),
    path('file_process/', views.show_list_of_files2process, name='file_process'),
    path('_file_process/<int:file_id>/', views.process_file, name='_file_process'),
    path('download_outputs/', views.download_all_outputs, name='download_all_outputs'),
    path('display_outputs/', views.display_output, name='display_outputs'),
    path('render_html_file/<str:output_folder>/', views.render_html_file, name='render_html_file'),
    path('render_html_file/<str:output_folder>/<str:image_name>/', views.serve_dynamic_image, name='serve_dynamic_image'),

]
