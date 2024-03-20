from django.shortcuts import render
from django.urls import path
from .models import Message
from django.http import HttpResponseRedirect
from django.urls import reverse
# 创建视图处理函数

def wikiTalk(request):
    messages = Message.objects.all()
    # for message in messages:
    #     message.pub_time
    #     pass
    return render(request,'wikiTalk.html',{'messages': messages})





def addMessage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        content = request.POST.get('content')
        message = Message()
        message.username = username
        message.content = content
        message.save()
        return HttpResponseRedirect(reverse('wikiTalk'))
    else:
        return render(request, 'add_message.html')