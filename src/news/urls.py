from django.urls import path
from .views import news_summary

app_name = 'news'

urlpatterns = [
    path('news_summary/', news_summary, name='news_summary'),
]
