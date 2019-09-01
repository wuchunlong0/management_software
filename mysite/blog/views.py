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

def index(request):
    return HttpResponse("index")


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
