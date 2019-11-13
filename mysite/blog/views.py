# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse, redirect
from .models import UserInfo, Role, Permission

# http://localhost:8000/sigin/
def sigin(request):        
    if request.method == "POST":
        username = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user = UserInfo.objects.filter(name=username, pwd=pwd).first()
        if user:
            request.session["user_id"] = user.pk
            permission_list = user.roles.all().values("permissions__url", "permissions__title").distinct()
            temp = []
            for per_url in permission_list:
                temp.append(per_url["permissions__url"])
            request.session["permissions_list"] = temp
            return HttpResponse("OK")
    return render(request, "blog/login.html")

def home(request):
    return render(request, 'blog/home.html', context=locals()) 

def contactus(request):
    if request.method != 'POST':
        return  render(request, 'blog/contactus.html', context=locals())  
    meg = '提交成功，我们将在24小时内联系您 ^o^'
    cleanData = request.POST.dict() 
    del cleanData['csrfmiddlewaretoken']       
    iscontact = Contacts.objects.filter(content = cleanData.get('content',''))
    if iscontact:
        meg = '已经提交过了，不要重复提交！我们将在24小时内联系您 ^o^'
    else:            
        c = Contacts(**cleanData)
        c.save()            
    return  render(request, 'blog/contactus.html', context=locals())  





# http://localhost:8000/user_list/
def user_list(request):
    return HttpResponse("user_list")

# http://localhost:8000/user_add/
def user_add(request):
    return HttpResponse("user_add")

# http://localhost:8000/user_edit/
def user_edit(request):
    return HttpResponse("user_edit")

# http://localhost:8000/user_del/
def user_del(request):
    return HttpResponse("user_del")
