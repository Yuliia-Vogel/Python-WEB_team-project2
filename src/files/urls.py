from django.urls import path
from .views import file_list, upload_file, download_file, delete_file

app_name = "files"

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'), 
    path("download/<int:file_id>/", download_file, name="download_file"),
    path("delete/<int:file_id>/", delete_file, name="delete_file"),
]
