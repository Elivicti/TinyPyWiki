from django.shortcuts import render,redirect
from django.utils.safestring import SafeText, mark_safe
from django.contrib.auth.decorators import login_required

from .models import WikiArticle, WikiArticleEditLog
from .utils import parse_markdown, find_in_markdown, make_formatted_time
from .forms import WikiEditorForm
from mainwiki.utils import get_section_tab

# Create your views here.

def get_article(request, article_title: str):
    try:
        articles = WikiArticle.objects.filter(title=article_title)
        articles = WikiArticleEditLog.objects.filter(article_id=articles[0].id).order_by("-edit_time")
        article = parse_markdown(articles[0].content)
    except Exception as e:
        print(e)
        return render(request, "base.html", {
            "var_title": article_title,
            "var_intro": SafeText("The article you are trying to find does not exist.<p><a href=\"edit\">Create This Page</a></p>"),
            "var_article": SafeText("<p style=\"height: 20em\"></p>"),
            "tab_sections": get_section_tab(request, article_title, active_section="read", force_hide_editor=True)
        })
    else:
        return render(request, "base.html", {
            "var_title": article.title,
            "var_intro": SafeText(article.intro),
            "var_contents": SafeText(article.contents_panel),
            "var_article": SafeText(article.article),
            "var_last_edit_time": make_formatted_time(articles[0].edit_time),
            "tab_sections": get_section_tab(request, article_title, "read"),
        })

@login_required(login_url="/user/login/")
def edit_article(request, article_title: str):
    try:
        article = WikiArticle.objects.filter(title=article_title)[0]
    except:
        article = WikiArticle()
        article.title = article_title
        article.save()

    if request.method == "GET":
        try:
            articles = WikiArticleEditLog.objects.filter(article_id=article.id).order_by("-edit_time")
            article_content = articles[0].content
        except:
            article_content = "# %s" % article_title
        editor_form = WikiEditorForm(initial={"editor": request.user, "article_id": article.id})

        return render(request, "editor.html", {
            "var_title": "Edit: %s" % article_title,
            "tab_sections": get_section_tab(request, article_title, "edit"),
            "article_content": article_content,
            "var_last_edit_time": make_formatted_time(articles[0].edit_time),
            "form" : editor_form
        })

    editor_form = WikiEditorForm(initial={"editor": request.user, "article_id": article.id}, data=request.POST)
    if editor_form.check():
        article.title = editor_form.title
        article.save()
        editor_form.save()
        return redirect("/a/%s/" % article.title)
    
    errors = []
    for field, error in editor_form.errors.items():
        if field == "commit_msg":
            errors.append("Commit message is required.")
        else:
            errors.append(error[0])

    return render(request, "editor.html", {
        "var_title": "Edit: %s" % article_title,
        "tab_sections": get_section_tab(request, article_title, "edit"),
        "article_content": request.POST["content"],
        "form" : WikiEditorForm(initial={"editor": request.user, "article_id": article.id}),
		"var_last_edit_time": make_formatted_time(articles[0].edit_time),
        "errors": errors
    })

    
def article_history(request, article_title: str):
    try:
        article = WikiArticle.objects.filter(title=article_title)
        article_log = WikiArticleEditLog.objects.filter(article_id=article[0].id).order_by("-edit_time")
    except:
        return redirect("/a/%s/" % article_title)
    
    return render(request, "history.html", {
        "var_title": "History: " + article_title,
        "tab_sections": get_section_tab(request, article_title, "history"),
		"var_last_edit_time": make_formatted_time(article_log[0].edit_time),
        "logs": article_log,
    })

def view_article_history(request, article_title: str, edit_id: int):
    articles = WikiArticleEditLog.objects.filter(id=edit_id).order_by("-edit_time")

    article = parse_markdown(articles[0].content)

    return render(request, "base.html", {
            "var_title": article.title,
            "var_intro": SafeText(article.intro),
            "var_contents": SafeText(article.contents_panel),
            "var_article": SafeText(article.article),
            "var_last_edit_time": make_formatted_time(articles[0].edit_time),
            "tab_sections": get_section_tab(request, article_title, "read"),
        })

def search_article(request):
    key_word = request.GET.get("param", "")
    if len(key_word) < 3:
        return render(request, "search.html", {
            "correct_error_tooltip": SafeText("<p class=\"django-form-8\">Please enter more than 2 characters.</p>")
        })

    search: dict[int, WikiArticleEditLog] = {}
    
    for obj in WikiArticleEditLog.objects.filter().order_by("-edit_time"):
        if obj.article_id not in search.keys():
            search[obj.article_id.id] = obj
    
    class SearchResult:
        def __init__(self, title: str, intro: str) -> None:
            self.title = title
            self.intro = intro

    results: list[SearchResult] = []
    for article_id, log in search.items():
        article = WikiArticle.objects.filter(id=article_id)[0]
        match = find_in_markdown(key_word, log.content)
        if match:
            results.append(SearchResult(article.title, match))
    
    return render(request, "search.html", {
        "var_title": "Search",
        
        "var_last_edit_time": make_formatted_time(),
        "tab_name_alt": "Search",
        "results": results
    })