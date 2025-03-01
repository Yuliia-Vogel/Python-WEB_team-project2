from django.urls import path
from .views import (
    RegisterView, LoginView, ChangePasswordView,
    PasswordResetConfirmView,
    register_page, login_page, registration_success_view,
    password_reset_form_view, password_reset_done_view, 
    password_reset_confirm_view, logout_view, password_reset_sent_view, password_reset_complete_view, password_reset_request
)

app_name = "users"

urlpatterns = [
    # API маршрути
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", login_page, name="login-page"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("password-reset-sent/", password_reset_sent_view, name="password_reset_sent"),
    path("password-reset-confirm/<uidb64>/<token>/", password_reset_confirm_view, name="password_reset_confirm"),
    path("password-reset-complete/", password_reset_complete_view, name="password_reset_complete"),

    # HTML сторінки
    path("register-page/", register_page, name="register_page"),
    path("login-page/", login_page, name="login_page"),
    path("logout/", logout_view, name="logout"),
    path("password-reset-form/", password_reset_form_view, name="password_reset_form"),
    path("registration-success/", registration_success_view, name="registration_success"),

    # Сторінки для відновлення пароля
    path("password-reset/", password_reset_request, name="password_reset"),
    path("password-reset-form/", password_reset_form_view, name="password_reset_form"),
    path("password-reset-sent/", password_reset_sent_view, name="password_reset_sent"),
    path("password-reset-confirm/<uidb64>/<token>/", password_reset_confirm_view, name="password_reset_confirm"),
    path("password-reset-complete/", password_reset_complete_view, name="password_reset_complete"),

    # Вихід з системи
    path("logout/", logout_view, name="logout"),
]
