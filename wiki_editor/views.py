from django.shortcuts import render,redirect
from django.utils.safestring import SafeText, mark_safe
from django.contrib.auth.decorators import login_required

from .models import WikiArticle, WikiArticleEditLog
from .utils import parse_markdown
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
            "var_last_edit_time": articles[0].edit_time.strftime("%Y-%m-%d, at %H:%M:%S (%Z)"),
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
            "form" : editor_form
        })

    editor_form = WikiEditorForm(initial={"editor": request.user, "article_id": article.id}, data=request.POST)
    if editor_form.check():
        article.title = editor_form.title
        article.save()
        editor_form.save()
        return redirect("/a/%s/" % article.title)
        
    print(editor_form.errors.items())
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
            "var_last_edit_time": articles[0].edit_time.strftime("%Y-%m-%d, at %H:%M:%S (%Z)"),
            "tab_sections": get_section_tab(request, article_title, "read"),
        })