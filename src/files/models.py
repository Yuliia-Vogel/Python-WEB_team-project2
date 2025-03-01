import cloudinary
from django.db import models
from django.contrib.auth import get_user_model

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

    def delete(self, *args, **kwargs):
        """Видалення файлів із Cloudinary перед видаленням запису з БД."""
        if self.public_id:
            try:
                cloudinary.uploader.destroy(self.public_id, resource_type="image") # Для зображень
                cloudinary.uploader.destroy(self.public_id, resource_type="video") # Для відео
                cloudinary.uploader.destroy(self.public_id, resource_type="raw") # Для всього іншого (документи, аудіо, архіви)
            except Exception as e:
                print(f"Error deleting {self.public_id} from Cloudinary: {e}") # Лог для відладки
        super().delete(*args, **kwargs)

    def get_filename(self):
        return self.file_url.split("/")[-1]

    def __str__(self):
        return f"{self.get_category_display()} file uploaded by {self.user}"
