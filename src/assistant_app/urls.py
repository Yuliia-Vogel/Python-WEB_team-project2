from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls", namespace="users")),  # Підключаємо маршрути користувачів
    path("notes/", include("notes.urls", namespace="notes")),  # Підключаємо маршрути нотаток
    path("contacts/", include("contacts.urls", namespace="contacts")),  # 📌 Додаємо namespace
    # path('users/', include("users.urls", namespace="users")),
    path("", home, name="home"),  # Головна сторінка
]
