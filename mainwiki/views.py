from django.shortcuts import render, redirect
from django.urls import path
from wiki_editor.mdhtml import parse_markdown
from django.utils.safestring import SafeText

# 创建视图处理函数
def home(request):
    return render(request, 'index.html')

def not_found(request):
    return render(request, "404.html")

def test_page(request):
    return render(request, "test.html", {
        "article_content": "this is content"
    })


def get_article(request, article_id: str):
    try:
        with open("assets/articles/%s.md" % article_id, "r") as f:
            article = parse_markdown(f)
    except:
        return redirect("/404/")
    else:
        return render(request, "base.html", {
            "var_title": article.title,
            "var_intro": SafeText(article.intro),
            "var_contents": SafeText(article.contents_panel),
            "var_article": SafeText(article.article),
        })