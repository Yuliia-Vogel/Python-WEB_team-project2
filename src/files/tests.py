from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from unittest.mock import patch
from files.models import UploadedFile

User = get_user_model()


class FileUploadTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.test_file = SimpleUploadedFile("test.txt", b"Hello, world!", content_type="text/plain")
        self.empty_file = SimpleUploadedFile("empty.txt", b"", content_type="text/plain")
        self.exe_file = SimpleUploadedFile("test.exe", b"dummy data", content_type="application/x-msdownload")

    @patch("cloudinary.uploader.upload")
    def test_upload_file_success(self, mock_upload):
        """Тест успішного завантаження файлу"""
        mock_upload.return_value = {"secure_url": "https://cloudinary.com/test_file", "public_id": "test123"}
        # це імітація завантаження файлу на клаудінері
        url = reverse("files:upload_file")
        response = self.client.post(url, {"file": self.test_file}) # запит через тестовий клієнт

        self.assertEqual(response.status_code, 200)
        self.assertEqual(UploadedFile.objects.count(), 1)
        file_obj = UploadedFile.objects.first()
        self.assertEqual(file_obj.file_url, "https://cloudinary.com/test_file")

    def test_upload_invalid_file(self):
        """Тест спроби завантажити невалідний файл (відсутній файл)"""
        url = reverse("files:upload_file")
        response = self.client.post(url, {})  # Без файлу в запиті
        self.assertEqual(response.status_code, 400)  # Очікуємо код 400 (Bad Request)

    def test_upload_empty_file(self):
        """Тест спроби завантажити порожній файл"""
        url = reverse("files:upload_file")
        response = self.client.post(url, {"file": self.empty_file})

        # Очікуємо, що відповідь буде 400, якщо файл порожній
        self.assertEqual(response.status_code, 200) # 200- це відповідь на повторний рендерінг html-сторінки
        self.assertContains(response, "The file is empty.")

    def test_upload_exe_file(self):
        """Тест спроби завантажити exe файл, що не дозволяється"""
        url = reverse("files:upload_file")
        response = self.client.post(url, {"file": self.exe_file})

        # Очікуємо, що файл з розширенням .exe буде відхилено
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "Exe files are not allowed to upload.")


class FileDownloadTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.file = UploadedFile.objects.create(
            # ставлю реальний урл до клаудінері, бо інакше постійно отримую 404 на тестовий урл:
            user=self.user, file_url="https://res.cloudinary.com/dud4xy94k/raw/upload/v1740835845/users_files/arwen.vogel%40gmail.com/archives/WEB%20project%20files.7z", public_id="test123"
        )

    def test_download_existing_file(self):
        """Тест скачування існуючого файлу"""
        url = reverse("files:download_file", kwargs={"file_id": self.file.id})
        print(f"File id = {self.file.id}")
        print(f"Public id = {self.file.public_id}")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Disposition"], f'attachment; filename="{self.file.get_filename()}"')


    def test_download_non_existing_file(self):
        """Тест скачування неіснуючого файлу"""
        url = reverse("files:download_file", kwargs={"file_id": 999}) # вказую неіснуючий файл
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


# class FileDeleteTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="password")
#         self.client.login(username="testuser", password="password")
#         self.file = File.objects.create(
#             user=self.user, file_url="https://cloudinary.com/test_file", public_id="test123"
#         )

#     @patch("cloudinary.uploader.destroy")
#     def test_delete_existing_file(self, mock_destroy):
#         """Тест видалення існуючого файлу"""
#         mock_destroy.return_value = {"result": "ok"}

#         url = reverse("files:delete", kwargs={"pk": self.file.pk})
#         response = self.client.delete(url)

#         self.assertEqual(response.status_code, 204)
#         self.assertFalse(File.objects.filter(pk=self.file.pk).exists())

#     def test_delete_non_existing_file(self):
#         """Тест видалення неіснуючого файлу"""
#         url = reverse("files:delete", kwargs={"pk": 999})
#         response = self.client.delete(url)

#         self.assertEqual(response.status_code, 404)


# class FileFilteringTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="password")
#         self.client.login(username="testuser", password="password")

#         File.objects.create(user=self.user, file_url="https://cloudinary.com/img.jpg", category="images")
#         File.objects.create(user=self.user, file_url="https://cloudinary.com/doc.pdf", category="documents")

#     def test_filter_by_category(self):
#         """Тест фільтрації файлів за категорією"""
#         url = reverse("files:list") + "?category=images"
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 1)
#         self.assertIn("img.jpg", response.json()[0]["file_url"])

#     def test_filter_without_category(self):
#         """Тест отримання всіх файлів, якщо категорія не вказана"""
#         url = reverse("files:list")
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 2)

#     def test_filter_invalid_category(self):
#         """Тест фільтрації за неіснуючою категорією"""
#         url = reverse("files:list") + "?category=nonexistent"
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.json()), 0)
