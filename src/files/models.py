import cloudinary.uploader 
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file_url = models.URLField()  # Зберігаємо в постгресі лише URL файлу на клаудінері
    public_id = models.CharField(max_length=255, unique=True)  # Додаємо public_id - для завантаження ІЗ клаудінері
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def delete(self, *args, **kwargs):
        """Видалення файлів із клаудінері перед видаленням запису з бази даних постгрес."""
        if self.public_id:
            try:
                cloudinary.uploader.destroy(self.public_id, resource_type="image")  # Для зображень
                cloudinary.uploader.destroy(self.public_id, resource_type="video")  # Для відео
                cloudinary.uploader.destroy(self.public_id, resource_type="raw")    # Для всього іншого (документи, аудіо, архіви)
            except Exception as e:
                print(f"Error deleting {self.public_id} from Cloudinary: {e}")  # Лог для відладки
        super().delete(*args, **kwargs)


    def __str__(self):
        return f"File uploaded by {self.user}"
