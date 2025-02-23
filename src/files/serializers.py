from rest_framework import serializers
from .models import UploadedFile

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at']

    def create(self, validated_data):
        request = self.context.get('request')  # Отримуємо request з контексту
        user = request.user  # Отримуємо користувача, який завантажує файл

        file = validated_data.pop('file')

        uploaded_file = UploadedFile(user=user)
        uploaded_file.save(file=file)  # Передаємо файл у `save()`
        return uploaded_file
