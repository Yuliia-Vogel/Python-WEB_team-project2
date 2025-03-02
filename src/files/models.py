import logging
import cloudinary
from django.db import models
from django.contrib.auth import get_user_model
from files.services import CloudinaryService

User = get_user_model()

CATEGORY_CHOICES = [
    ("images", "Images"),
    ("documents", "Documents"),
    ("videos", "Videos"),
    ("audio", "Audio"),
    ("archives", "Archives"),
    ("other", "Other"),
]

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file_url = models.URLField()  
    public_id = models.CharField(max_length=255, unique=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    file_name = models.CharField(max_length=255, null=True, blank=True)  # нове поле
    resource_type = models.CharField(max_length=50, null=True, blank=True)  # нове поле

    def delete(self, *args, **kwargs):
        print(f"Models. Attempting to delete file with public_id: {self.public_id}")
        """Видалення файлів із Cloudinary перед видаленням запису з БД."""
        if self.public_id:
            try:
                logger = logging.getLogger(__name__)
                logger.info(f"Public id: {self.public_id}")
                print("Before Cloudinary delete")
                # cloudinary.uploader.destroy(self.public_id, resource_type="image") # Для зображень
                # cloudinary.uploader.destroy(self.public_id, resource_type="video") # Для відео
                # cloudinary.uploader.destroy(self.public_id, resource_type="raw") # Для всього іншого (документи, аудіо, архіви)
                # Видаляємо тільки з правильним resource_type
                # Спочатку перевіряємо тип ресурсу
                if not self.resource_type:
                    # Якщо ресурсний тип не вказаний, визначаємо його
                    self.resource_type = CloudinaryService.get_resource_type(self.file_name)
                # Тепер видаляємо файл з Cloudinary
                cloudinary.uploader.destroy(self.public_id, resource_type=self.resource_type)
                print("After Cloudinary delete")
                logger.info(f"Models. File with public_id: {self.public_id} deleted successfully")

            except Exception as e:
                logger.info(f"Models. Error deleting {self.public_id} from Cloudinary: {e}") 
        print("Before super delete")
        super().delete(*args, **kwargs)
        print("After super delete")
            

    def get_filename(self):
        return self.file_url.split("/")[-1]

    def __str__(self):
        return f"{self.get_category_display()} file uploaded by {self.user}"
