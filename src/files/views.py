import os
import logging
import requests
from django.http import JsonResponse
import cloudinary.uploader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import UploadedFile

CATEGORY_MAP = {
    "images": ["jpg", "jpeg", "png", "gif", "webp", "svg"],
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "txt", "ppt", "pptx"],
    "videos": ["mp4", "avi", "mov", "mkv", "flv", "wmv"],
    "audio": ["mp3", "wav", "ogg", "flac", "aac", "m4a"],
    "archives": ["zip", "rar", "7z", "tar", "gz"],
}

FORBIDDEN_EXTENSIONS = ['.exe']

logger = logging.getLogger(__name__)

def get_file_category(filename):
    ext = filename.split(".")[-1].lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return "other"


def check_file_size(uploaded_file):
    # Ліміти для різних типів файлів
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 MB
    MAX_RAW_SIZE = 10 * 1024 * 1024  # 10 MB

    file_name, file_extension = os.path.splitext(uploaded_file.name)

    # Перевірка на розмір файлу для різних типів
    if 'image' in uploaded_file.content_type:
        if uploaded_file.size > MAX_IMAGE_SIZE:
            return False, "Image file size too large. Maximum size is 10 MB."
    elif 'video' in uploaded_file.content_type:
        if uploaded_file.size > MAX_VIDEO_SIZE:
            return False, "Video file size too large. Maximum size is 100 MB."
    else:
        if uploaded_file.size > MAX_RAW_SIZE:
            return False, "Raw file size too large. Maximum size is 10 MB."

    return True, None


@login_required
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({"error": "File is required"}, status=400)

        uploaded_file = request.FILES['file']
        
        # Перевірка на порожній файл
        if uploaded_file.size == 0:
            form = UploadFileForm()  # Повторно ініціалізуємо форму, щоб не було помилки при рендерингу
            return render(request, 'assistant_app/upload_file.html', {
                'form': form,
                'error': "The file is empty."  # Передаємо повідомлення про помилку
            })
        
        # Перевірка розміру файлу
        is_valid, error_message = check_file_size(uploaded_file)
        if not is_valid:
            form = UploadFileForm()
            return render(request, 'assistant_app/upload_file.html', {
                'form': form,
                'error': error_message
            })

        # Перевірка на заборонене розширення
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        if file_extension.lower() in FORBIDDEN_EXTENSIONS:
            form = UploadFileForm()  # Повторно ініціалізуємо форму
            return render(request, 'assistant_app/upload_file.html', {
                'form': form,
                'error': "Exe files are not allowed to upload."  # Повідомлення про заборонений файл
            })

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            category = get_file_category(uploaded_file.name)
            folder_name = f"users_files/{request.user.email}/{category}"
            uploaded_data = cloudinary.uploader.upload(
                uploaded_file,
                folder=folder_name,
                resource_type='auto',
                public_id=uploaded_file.name
            )
            logger.info(f"Uploading: {uploaded_file.name}")
            UploadedFile.objects.create(user=request.user, 
                                        file_url=uploaded_data["secure_url"],
                                        public_id=uploaded_data["public_id"])

            return render(request, 'assistant_app/upload_success.html', {
                'file_name': uploaded_file.name,
                'file_url': uploaded_data["secure_url"]
            })

    else:
        form = UploadFileForm()
    return render(request, 'assistant_app/upload_file.html', {'form': form})


@login_required
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)  # Фільтруємо файли поточного юзера
    category = request.GET.get("category", "all")  # Отримуємо категорію з GET-запиту

    valid_files = []

    for file in files:
        try:
            response = requests.head(file.file_url, timeout=5)  # Перевіряємо чи файл існує
            if response.status_code == 200:
                # Отримуємо назву папки з URL файлу
                folder_name = file.file_url.split("/")[-2]  # передостанній елемент - це папка

                # Фільтруємо за категорією
                if category == "all" or folder_name == category:
                    valid_files.append(file)
        except requests.RequestException:
            pass  # Файл не знайдено або інша помилка

    return render(request, "assistant_app/file_list.html", {
        "files": valid_files,
        "selected_category": category
    })


@login_required
def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    file_url = file.file_url
    logger.info(f"Attempting to download file with ID {file_id}, URL: {file_url}")

    if not file_url:
        logger.error(f"File URL not found for file ID {file_id}")
        return HttpResponse("File not found", status=404)

    try:
        # Виконуємо запит для отримання файлу з Cloudinary
        response = requests.get(file_url, stream=True)
        logger.info(f"Received response from Cloudinary with status code {response.status_code}")


        # Якщо файл знайдений, відповідаємо з контентом
        if response.status_code == 200:
            logger.info(f"File found, preparing for download")
            response = HttpResponse(response.content, content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{file_url.split("/")[-1]}"'
            return response
        else:
            logger.error(f"Error from Cloudinary, status code: {response.status_code}")
            # Якщо сервер Cloudinary повернув помилку (наприклад, 404 або інші), повертаємо помилку
            return HttpResponse("File not found on Cloudinary", status=404)
    
    except requests.exceptions.RequestException as e:
        # Якщо виникла помилка при виконанні запиту (наприклад, проблема з мережею)
        logger.error(f"Error occurred while retrieving the file: {str(e)}")
        return HttpResponse(f"Error occurred while retrieving the file: {str(e)}", status=503)
    

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)

    logger.info(f"Deleting: {file.public_id}")

    # просто видаляємо об'єкт, і `delete()` сам подбає про Cloudinary (бо ми перевизначили функцію видалення в класі UploadedFile)
    file.delete()

    return render(request, 'assistant_app/file_deleted.html')


