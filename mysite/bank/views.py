# -*- coding: utf-8 -*-
import os
from django.conf import settings
#import re
from django.shortcuts import render, HttpResponse, redirect
from .models import Bankemploye, Bankuser, Contacts, Setvalue
from rbac.models import UserInfo
import xlrd
import json
from myAPI.excelAPI import list_to_xlsx, list_to_htmlTableStr
from myAPI.listAPI import get_sum
from myAPI.dictAPI import dict_sorted
from myAPI.listdictAPI import listdictTolists
from myAPI.downfileAPI import down_file
from myAPI.fileAPI import  MyFile, zipDir, readJson
from docx.shared import Mm, Inches, Pt
from docxtpl import DocxTemplate, InlineImage
from decimal import *

import matplotlib.pyplot as plt

from pylab import mpl,np
PATH_MD = 'bank/files/md/'

def test(request):
    meg = 'test  ^o^'
    return render(request, 'layout2.html', context=locals()) 
    return render(request, 'bank/excel_import.html', context=locals()) 

def index(request):         
    Systematic_Introduction = open('%s系统简介.md' %PATH_MD, 'r').read() 
    return render(request, 'bank/index.html', context=locals())  
           
def help(request, s_name):
    """帮助文档"""    
    if s_name == '(.+)' or s_name == 'menu':
        title_yield = MyFile('bank/static/menu', ['.md']).get_openTxt()
        return render(request, 'bank/help/menu.html', context=locals()) 
        
    meg = ' ^o^'
    return render(request, 'bank/excel_import.html', context=locals())       



def upload(request):
     
    context = {'status': True, 'msg': ''}
    if request.method == "POST":   
        myFile = request.FILES.get("myfile", None)    
        if not myFile:
            context = {'status': True, 'msg': '没有选择文件！上传失败'}  
            return  render(request, 'bank/upload.html', context=locals())  
        if 'doc' not in myFile.name and 'docx' not in myFile.name:
            context = {'status': True, 'msg': '请选择Word文件,扩展名为.doc 或 .docx！上传失败'} 
            return  render(request, 'bank/upload.html', context=locals()) 
        f = open(TPL_FILE,'wb+') #TPL_FILE='web/files/分析报告模板.docx' 
        for chunk in myFile.chunks():      
            f.write(chunk)  
        f.close()
        context = {'status': True, 'msg': '上传成功. %s' %TPL_FILE }
    return  render(request, 'bank/upload.html', context) 
    return  render(request, 'bank/upload.html', context=locals())

def download(request):
    tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files',\
                             'AnalysisReport.docx')
    tpl_path = TPL_FILE
    if not os.path.exists(tpl_path):
        meg = '%s 文件不存在。  ^o^' %tpl_path
        return render(request, 'bank/excel_import.html', context=locals())         
    return down_file(tpl_path, 'tpl_word.docx')
