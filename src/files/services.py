import os
import uuid
import logging
import cloudinary.uploader
from urllib.parse import urlparse
from django.db.utils import IntegrityError
# from files.models import UploadedFile


CATEGORY_MAP = {
    "images": ["jpg", "jpeg", "png", "gif", "webp", "svg"],
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "txt", "ppt", "pptx"],
    "videos": ["mp4", "avi", "mov", "mkv", "flv", "wmv"],
    "audio": ["mp3", "wav", "ogg", "flac", "aac", "m4a"],
    "archives": ["zip", "rar", "7z", "tar", "gz"],
}

FORBIDDEN_EXTENSIONS = ['.exe', '.bat']

class CloudinaryService:
    @staticmethod
    def upload_file(uploaded_file, user_email):
        from files.models import UploadedFile  # Lazy Import - імпорт тут, щоб уникнути циклічного імпорту
         # Перевірка на заборонені розширення
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        if file_extension.lower() in FORBIDDEN_EXTENSIONS:
            raise ValueError(f"File extension {file_extension} is not allowed.")
        
        category = CloudinaryService.get_file_category(uploaded_file.name)
        folder_name = f"users_files/{user_email}/{category}"
        file_name, _ = os.path.splitext(uploaded_file.name)

        # Перевіряємо, чи існує вже файл з таким іменем у Cloudinary
        existing_files = cloudinary.api.resources(type="upload", prefix=folder_name)
        existing_files_names = [file['public_id'] for file in existing_files['resources']]

        # Якщо файл з таким public_id вже є, додаємо унікальний суфікс
        if file_name in existing_files_names:
            unique_suffix = uuid.uuid4().hex[:8]
            file_name = f"{file_name}_{unique_suffix}"


        # public_id = f"{folder_name}/{file_name}"
        public_id = file_name

        uploaded_data = cloudinary.uploader.upload(
            uploaded_file,
            folder=folder_name,
            resource_type='auto', # а чи не тут криється проблема з видаленням?
            public_id=public_id
        )

        return uploaded_data["secure_url"], uploaded_data["public_id"], category

    @staticmethod
    def get_file_category(filename):
        ext = filename.split(".")[-1].lower()
        for category, extensions in CATEGORY_MAP.items():
            if ext in extensions:
                return category
        return "other"

    @staticmethod
    def extract_folder_from_url(file_url):
        path_parts = urlparse(file_url).path.strip("/").split("/")
        return path_parts[-2] if len(path_parts) > 1 else None

    @staticmethod
    def check_file_size(uploaded_file):
        MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB
        MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 MB
        MAX_RAW_SIZE = 10 * 1024 * 1024  # 10 MB

        if 'image' in uploaded_file.content_type:
            return uploaded_file.size <= MAX_IMAGE_SIZE, "Image file size too large. Maximum size is 10 MB."
        elif 'video' in uploaded_file.content_type:
            return uploaded_file.size <= MAX_VIDEO_SIZE, "Video file size too large. Maximum size is 100 MB."
        else:
            return uploaded_file.size <= MAX_RAW_SIZE, "File size too large. Maximum size is 10 MB."

        return True, None
    
    @staticmethod
    def get_resource_type(filename: str) -> str:
        """
        Визначає тип ресурсу на основі розширення файлу.
        Повертає 'image', 'video', 'raw' або 'unknown'.
        """
        ext = filename.split(".")[-1].lower()
        
        # Картки типів
        image_extensions = ["jpg", "jpeg", "png", "gif", "webp", "svg"]
        video_extensions = ["mp4", "avi", "mov", "mkv", "flv", "wmv"]
        
        # Визначаємо тип на основі розширення
        if ext in image_extensions:
            return "image"
        elif ext in video_extensions:
            return "video"
        else:
            return "raw"

    @staticmethod
    def remove_extension_for_non_raw_file(name: str) -> str:
        """
        Видаляє розширення з імені файлу для файлів, які не є raw.
        Це допомагає уникнути подвійного розширення в Cloudinary URL.
        """
        file_resource_type = CloudinaryService.get_resource_type(name)  # викликаємо метод класу
        if file_resource_type == "raw":
            return name
        else:
            # Видалення розширення
            extension = name.split('.')[-1]
            return name[:-(len(extension) + 1)]  # видаляємо розширення з імені файлу

    @staticmethod
    def delete_file(public_id, resource_type):
        print(f"Public_id = {public_id}, resource_type = {resource_type}")
        try:
            logger = logging.getLogger(__name__)
            logger.info(f"Services. Attempting to delete file with : {public_id}")

            # Перевірка, чи дійсно файл існує на Cloudinary
            result = cloudinary.api.resource(public_id, resource_type=resource_type)
            logger.info(f"Services. Cloudinary resource check response: {result}")

            if result.get("error"):
                return False, f"Services. Error fetching resource: {result['error']}"

            if result.get("result") == "not found":
                return False, f"Services. File with public_id {public_id} not found on Cloudinary"

            # Якщо файл знайдений, то його видаляємо
            result = cloudinary.uploader.destroy(public_id, invalidate=True, resource_type=resource_type)
            logger.info(f"Services. Cloudinary response: {result}, response: {result}")

            if result.get("result") == "ok":
                return True, None
            else:
                return False, f"Services. Failed to delete file from Cloudinary, response: {result}"
        except cloudinary.exceptions.NotFound as e:
            logger.error(f"Services. File not found on Cloudinary: {e}")
            return False, "File not found on Cloudinary"
    
        except Exception as e:
            logger.error(f"Services. Unexpected error while deleting file: {e}")
            return False, str(e)

    # @staticmethod
    # def delete_file(public_id, resource_type="raw"):
    #     try:
    #         print(f"Services. Attempting to delete file with : {public_id}")
    #         response = cloudinary.api.delete_resources(
    #             [public_id], resource_type=resource_type, invalidate=True
    #         )
    #         print(f"Services. Cloudinary delete response: {response}")
    #         return response
    #     except cloudinary.api.NotFound:
    #         print(f"Services. File not found on Cloudinary: {public_id}")
    #         return None  # Просто повертаємо None, щоб не падало з 500
    #     except Exception as e:
    #         print(f"Services. Unexpected error while deleting {public_id}: {e}")
    #         return None