from django.shortcuts import render, redirect
from django.urls import path

# 创建视图处理函数
def home(request):
    return render(request, 'index.html')

def not_found(request):
    return render(request, "404.html")

def test_page(request):
    return render(request, "test.html", {
        "article_content": "this is content"
    })

