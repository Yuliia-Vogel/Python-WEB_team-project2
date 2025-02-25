from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file_url = models.URLField()  # Зберігаємо в постгресі лише URL файлу на клаудінері
    public_id = models.CharField(max_length=255, unique=True)  # Додаємо public_id - для завантаження ІЗ клаудінері
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded by {self.user}"
