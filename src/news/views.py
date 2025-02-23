from django.shortcuts import render

def news_summary(request):
    return render(request, 'news/news_summary.html')
