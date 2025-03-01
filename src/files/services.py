import os
import logging
import cloudinary.uploader
from urllib.parse import urlparse

CATEGORY_MAP = {
    "images": ["jpg", "jpeg", "png", "gif", "webp", "svg"],
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "txt", "ppt", "pptx"],
    "videos": ["mp4", "avi", "mov", "mkv", "flv", "wmv"],
    "audio": ["mp3", "wav", "ogg", "flac", "aac", "m4a"],
    "archives": ["zip", "rar", "7z", "tar", "gz"],
}

FORBIDDEN_EXTENSIONS = ['.exe']

class CloudinaryService:
    @staticmethod
    def upload_file(uploaded_file, user_email):
        category = CloudinaryService.get_file_category(uploaded_file.name)
        folder_name = f"users_files/{user_email}/{category}"

        uploaded_data = cloudinary.uploader.upload(
            uploaded_file,
            folder=folder_name,
            resource_type='auto',
            public_id=uploaded_file.name
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
    def delete_file(public_id):
        try:
            logger = logging.getLogger(__name__)
            logger.info(f"Attempting to delete file with public_id: {public_id}")
            result = cloudinary.uploader.destroy(public_id)
            logger.info(f"Cloudinary response: {result}")
            if result.get("result") == "ok":
                return True, None
            else:
                return False, "Failed to delete file from Cloudinary"
        except Exception as e:
            return False, str(e)