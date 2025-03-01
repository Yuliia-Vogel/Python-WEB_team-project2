import os
import logging
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UploadedFile
from .forms import UploadFileForm
from .services import CloudinaryService

logger = logging.getLogger(__name__)

FORBIDDEN_EXTENSIONS = ['.exe']

class UploadFileView(LoginRequiredMixin, View):
    template_name = "assistant_app/upload_file.html"

    def get(self, request):
        return render(request, self.template_name, {'form': UploadFileForm()})

    def post(self, request):
        if 'file' not in request.FILES:
            return JsonResponse({"error": "File is required"}, status=400)

        uploaded_file = request.FILES['file']

        if uploaded_file.size == 0:
            return render(request, self.template_name, {'form': UploadFileForm(), 'error': "The file is empty."})

        is_valid, error_message = CloudinaryService.check_file_size(uploaded_file)
        if not is_valid:
            return render(request, self.template_name, {'form': UploadFileForm(), 'error': error_message})

        file_name, file_extension = os.path.splitext(uploaded_file.name)
        if file_extension.lower() in FORBIDDEN_EXTENSIONS:
            return render(request, self.template_name, {'form': UploadFileForm(), 'error': "Exe files are not allowed."})

        secure_url, public_id, category = CloudinaryService.upload_file(uploaded_file, request.user.email)

        UploadedFile.objects.create(
            user=request.user,
            file_url=secure_url,
            public_id=public_id,
            category=category
        )

        return render(request, 'assistant_app/upload_success.html', {'file_name': uploaded_file.name, 'file_url': secure_url})


class FileListView(LoginRequiredMixin, View):
    template_name = "assistant_app/file_list.html"

    def get(self, request):
        category = request.GET.get("category", "all")
        files = UploadedFile.objects.filter(user=request.user)

        if category != "all":
            files = files.filter(category=category)

        return render(request, self.template_name, {"files": files, "selected_category": category})


class DownloadFileView(LoginRequiredMixin, View):
    def get(self, request, file_id):
        file = get_object_or_404(UploadedFile, id=file_id)
        response = requests.get(file.file_url, stream=True)

        if response.status_code == 200:
            res = HttpResponse(response.content, content_type="application/octet-stream")
            res['Content-Disposition'] = f'attachment; filename="{file.get_filename()}"'
            return res
        return HttpResponse("File not found", status=404)


class DeleteFileView(LoginRequiredMixin, View):
    def post(self, request, file_id):
        file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
        
        # Видалення файлу з Cloudinary
        success, error_message = CloudinaryService.delete_file(file.public_id)

        if not success:
            return JsonResponse({"error": error_message}, status=500)

        # Видалення файлу з бази даних
        file.delete()

        return render(request, 'assistant_app/file_deleted.html')
