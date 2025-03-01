from django.urls import path
from .views import UploadFileView, FileListView, DownloadFileView, DeleteFileView

app_name = "files"

urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='upload_file'),
    path('files/', FileListView.as_view(), name='file_list'), 
    path("download/<int:file_id>/", DownloadFileView.as_view(), name="download_file"),
    path("delete/<int:file_id>/", DeleteFileView.as_view(), name="delete_file"),
]
