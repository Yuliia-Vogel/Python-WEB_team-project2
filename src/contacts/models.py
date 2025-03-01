from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='contacts',
        null=False,
        blank=False
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
