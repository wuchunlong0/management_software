# -*- coding: utf-8 -*-
# 测试样本：140_20_20.xlsx
import os
from django.conf import settings
#import re
from django.shortcuts import render, HttpResponse, redirect
from .models import Bankemploye, Bankuser, Contacts, Setvalue
from rbac.models import UserInfo
import xlrd
import json
from myAPI.excelAPI import post_excel_model, list_to_xlsx, list_to_htmlTableStr
from myAPI.listAPI import get_sum
from myAPI.dictAPI import dict_sorted
from myAPI.listdictAPI import listdictTolists
from myAPI.downfileAPI import down_file
from myAPI.fileAPI import  MyFile, zipDir, readJson
from docx.shared import Mm, Inches, Pt
from docxtpl import DocxTemplate, InlineImage
from decimal import *
#import mimetypes
#from django.http import JsonResponse
import matplotlib.pyplot as plt
#from matplotlib import pylab
from pylab import mpl,np
PATH_XLSX = 'web/download_excel/'
DOWNLOAD_EXCEL_FILE = 'web/download_excel.zip'
PATH_TXT = 'bank/files/txt/'
PATH_IMG = 'bank/files/img/'
TPL_FILE =  'web/files/分析报告模板.docx'  


#dict12345 = {'1':'非常差', '2':'较差','3':'一般','4':'敬业','5':'非常敬业'}

#满意度调查
dict12345 = {'1':'非常不满意', '2':'不满意','3':'一般','4':'满意','5':'非常满意'}


def test(request):
    meg = 'test  ^o^'
    return render(request, 'bank/excel_import.html', context=locals()) 


def index(request):         
    Systematic_Introduction = open('%s系统简介.md' %PATH_TXT, 'r').read() 
    technical_standard = open('%s技术标准.md' %PATH_TXT, 'r').read() 
    table_abcde = list_to_htmlTableStr(readJson('%stable_abcde.json' %PATH_TXT))
    table_per = list_to_htmlTableStr(readJson('%stable_per.json' %PATH_TXT))
    return render(request, 'bank/index.html', context=locals())  
           
def get_per():
    """[20.00, 15.00, 32.00, 20.18, 40.32]"""
    return  [Setvalue.objects.get(myid=0).a_per,\
            Setvalue.objects.get(myid=0).b_per,\
            Setvalue.objects.get(myid=0).c_per,\
            Setvalue.objects.get(myid=0).d_per,\
            Setvalue.objects.get(myid=0).e_per,]

def setting_list(request):
    '''显示阀值'''
    data = get_per()
    dataX = json.dumps(list(range(1, len(data)+1)))
    data = json.dumps(data)
    name = '设置阀值'  
    return render(request, 'bank/setting_list.html', context=locals())
    
    
def setting_value(request):
    '''
    设置阀值成功   数据库
    '''
    if request.method == 'POST':
        cleanData = request.POST.dict()
        del cleanData['csrfmiddlewaretoken']
        Setvalue.objects.all().delete()
        s = Setvalue(**cleanData)
        s.save()
        return redirect("/bank/setting/list/")
    per_list = range(5,105,5)
    return render(request, 'bank/setting_value.html', context=locals())     
         
def data_statistics(): 
    """ 问卷数据统计   按照1,2,3,4,5五个层次,进行人数、人数百分比统计，结果写入数据库Bankemploye """   
    user_sum = get_user_num()
    titles = get_sort_titles()
    if not user_sum:  return  user_sum, titles     
    for title in titles:
        reply_list = get_reply_list(title)
        id = Bankuser.objects.filter(title=title).first().id
        for (index,reply) in enumerate(reply_list):
            ask = Bankuser.objects.filter(id=id+index).first().ask 
            d = {'id':index,'sum':user_sum,'a':0,'b':0,'c':0,'d':0,'e':0,'title':ask}
            for r in reply:
                if 1 == r: d['a'] += 1
                if 2 == r: d['b'] += 1
                if 3 == r: d['c'] += 1
                if 4 == r: d['d'] += 1
                if 5 == r: d['e'] += 1
            d = {'a':d['a'], 'b':d['b'], 'c':d['c'], 'd':d['d'], 'e':d['e']}
            d.update({'a_per':str(Decimal(d['a']*100.0/user_sum).quantize(Decimal('0.00'))),\
                     'b_per':str(Decimal(d['b']*100.0/user_sum).quantize(Decimal('0.00'))),\
                     'c_per':str(Decimal(d['c']*100.0/user_sum).quantize(Decimal('0.00'))),\
                     'd_per':str(Decimal(d['d']*100.0/user_sum).quantize(Decimal('0.00'))),\
                     'e_per':str(Decimal(d['e']*100.0/user_sum).quantize(Decimal('0.00')))})            
            Bankemploye.objects.filter(investigation=ask).update(**d)
    return  user_sum, titles       

def context_dict(user_num):
    """
    print(context_dict())
    {'table_4_1': [{'e': 5, 'a': 11, 'sum': 30, 'b': 6, 'c': 4, 'title': '员工对分行的技术和工具使员工能够成功地开展工作有何评价？', 'id': 0, 'd': 4},  ...],  
    'table_4_title': '员工满意度调查1',
    ...
    'table_5_2': [{'e': 33.33, 'a': 16.67, 'sum': 30, 'b': 26.67, 'c': 13.33, 'title': '2员工对分行提供适合员工工作类型的社会信息有何评价？', 'id': 0, 'd': 10.0},  ...]
    }
    
    """    
    all_abcde = get_abcde('')
    all_abcde_per = get_abcde('per')
    abcde_len, abcde_per_len = len(all_abcde), len(all_abcde_per)    
    context = {}
    if abcde_len >= 1:
        context1 = {
            'table_4_title': list(all_abcde[0].keys())[0],
            'table_4_1': list(all_abcde[0].values())[0],
            'table_4_2': list(all_abcde_per[0].values())[0],        
        }       
        context.update(context1)
    
    if abcde_len >= 2:
        context2 = {
            'table_5_title': list(all_abcde[1].keys())[0],
            'table_5_1': list(all_abcde[1].values())[0],
            'table_5_2': list(all_abcde_per[1].values())[0],        
        }               
        context.update(context2)       
    
    if abcde_len >= 3:
        context3 = {
            'table_6_title': list(all_abcde[2].keys())[0],
            'table_6_1': list(all_abcde[2].values())[0],
            'table_6_2': list(all_abcde_per[2].values())[0],        
        }       
        context.update(context3)    
    context.update({'len' : abcde_len})
    context.update({'user_num' : user_num})
    return context

def saveNumImgFile(saveFile, title, abcde, user_sum):
    """
    按人数 保存为图片
    saveFile = ''
    user_sum = 30
    title 问卷题
    abcde = [5,3,4,5,5]
    
    from pylab import mpl
    import matplotlib.pyplot as plt
    
    """
    try:
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False    
        y_list =  range(0,user_sum+1)            
        fig, ax = plt.subplots()    
        bar_positions = [1,2,3,4,5]
        bar_heights = abcde
        ax.bar(np.arange(6),[0]+abcde, 0.6)#设置x，y数据，区间， 0.6竖线粗细
        ax.set_xticks([1,2,3,4,5])#设置x轴刻度
        ax.set_yticks(y_list)#设置y轴刻度
        ax.set_ylim(0, user_sum)#设置y轴范围
        ax.set_xlim(0, 6)#设置x轴范围，当然轴数据范围跟 坐标刻度不要冲突就好
        ax.set_facecolor("orange")#设置背景颜色为橙色    
        plt.title('%s'%title)
        plt.xlabel("   非常不满意      不满意       一般        满意       非常满意")
        plt.ylabel('   人 数')
        for a,b in zip(bar_positions,bar_heights):#显示数据标签 zip([1,2],[3,4]) = [(1,3),(2,4)]
            plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=12)
        plt.savefig(saveFile)#保存图片
        return True
    except Exception as ex:
        print('err: %s' %ex) 
        return False 
      
def savePerImgFile(saveFile, title, abcde_per):
    """
    按百分比 保存为图片
    saveFile = ''
    title 问卷题
    abcde_per = [27.00,33.00,10.00,15.00,15.00]
    
    from pylab import mpl
    import matplotlib.pyplot as plt
    
    """
    try:
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False    
        y_list =  range(0,101,5)            
        fig, ax = plt.subplots()    
        bar_positions = [1,2,3,4,5]
        bar_heights = abcde_per
        ax.bar(np.arange(6),[0]+abcde_per, 0.6)#设置x，y数据，区间， 0.6竖线粗细
        ax.set_xticks([1,2,3,4,5])#设置x轴刻度
        ax.set_yticks(y_list)#设置y轴刻度
        ax.set_ylim(0, 100)#设置y轴范围
        ax.set_xlim(0, 6)#设置x轴范围，当然轴数据范围跟 坐标刻度不要冲突就好
        ax.set_facecolor("orange")#设置背景颜色为橙色    
        plt.title('%s'%title)
        plt.xlabel("   非常不满意      不满意       一般        满意       非常满意")
        plt.ylabel('   百分比%')
        for a,b in zip(bar_positions,bar_heights):#显示数据标签 zip([1,2],[3,4]) = [(1,3),(2,4)]
            plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=12)
        plt.savefig(saveFile)#保存图片
        return True
    except Exception as ex:
        print('err: %s' %ex) 
        return False 

#'非常不满意', '2':'不满意','3':'一般','4':'满意','5':'非常满意'
def get_title_abcde():
    """    
    test: 10.xlsx
    mylist_abcde=[{'员工对分行的技术和工具使员工能够成功地开展工作有何评价？': [6, 9, 2, 7, 6]},
     {'员工对能够及时获得足够有效的信息以有效地完成工作有何评价？': [3, 5, 8, 7, 7]},  ... ]     
    mylist_abcde_analyse=[{'title': '员工对分行的技术和工具使员工能够成功地开展工作有何评价？', 
    'a_analyse': 'a00', 'b_analyse': 'b00', 'c_analyse': 'c00', 'd_analyse': 'd00', 
    'e_analyse': 'e00'}, ... ]
    """
    mylist_abcde = []
    mylist_abcde_per = []
    mylist_abcde_analyse = []
    try:
        count = Bankemploye.objects.filter().count()
        for n in range(0, count):
            mylist_abcde.append({Bankemploye.objects.get(serialNumber=n).investigation :\
                       [Bankemploye.objects.get(serialNumber=n).a,\
                       Bankemploye.objects.get(serialNumber=n).b,\
                       Bankemploye.objects.get(serialNumber=n).c,\
                       Bankemploye.objects.get(serialNumber=n).d,\
                       Bankemploye.objects.get(serialNumber=n).e]})
            mylist_abcde_per.append({Bankemploye.objects.get(serialNumber=n).investigation :\
                       [Bankemploye.objects.get(serialNumber=n).a_per,\
                       Bankemploye.objects.get(serialNumber=n).b_per,\
                       Bankemploye.objects.get(serialNumber=n).c_per,\
                       Bankemploye.objects.get(serialNumber=n).d_per,\
                       Bankemploye.objects.get(serialNumber=n).e_per]})
            mydict_abcde_analyse = {}
            mydict_abcde_analyse.update({'title' : Bankemploye.objects.get(serialNumber=n).investigation,})
            # >阀值 输出
            per_list = get_per()
                        
            if Bankemploye.objects.get(serialNumber=n).a_per >= per_list[0]:
                mydict_abcde_analyse.update({'a_analyse' : Bankemploye.objects.get(serialNumber=n).a_analyse})
                mydict_abcde_analyse.update({'a_per' : '%s%%的答卷人'%Bankemploye.objects.get(serialNumber=n).a_per})
            else:
                mydict_abcde_analyse.update({'a_analyse' : ''})
                mydict_abcde_analyse.update({'a_per' : ''})
            if Bankemploye.objects.get(serialNumber=n).b_per >= per_list[1]:
                mydict_abcde_analyse.update({'b_analyse' : Bankemploye.objects.get(serialNumber=n).b_analyse})
                mydict_abcde_analyse.update({'b_per' : '%s%%的答卷人'%Bankemploye.objects.get(serialNumber=n).b_per})
            else:
                mydict_abcde_analyse.update({'b_analyse' : ''})
                mydict_abcde_analyse.update({'b_per' : ''})
            if Bankemploye.objects.get(serialNumber=n).c_per >= per_list[2]:
                mydict_abcde_analyse.update({'c_analyse' : Bankemploye.objects.get(serialNumber=n).c_analyse})
                mydict_abcde_analyse.update({'c_per' : '%s%%的答卷人'%Bankemploye.objects.get(serialNumber=n).c_per})
            else:
                mydict_abcde_analyse.update({'c_analyse' : ''})
                mydict_abcde_analyse.update({'c_per' : ''})
            if Bankemploye.objects.get(serialNumber=n).d_per >= per_list[3]:
                mydict_abcde_analyse.update({'d_analyse' : Bankemploye.objects.get(serialNumber=n).d_analyse})
                mydict_abcde_analyse.update({'d_per' : '%s%%的答卷人'%Bankemploye.objects.get(serialNumber=n).d_per})
            else:
                mydict_abcde_analyse.update({'d_analyse' : ''})
                mydict_abcde_analyse.update({'d_per' : ''})
            if Bankemploye.objects.get(serialNumber=n).e_per >= per_list[4]:
                mydict_abcde_analyse.update({'e_analyse' : Bankemploye.objects.get(serialNumber=n).e_analyse})
                mydict_abcde_analyse.update({'e_per' : '%s%%的答卷人'%Bankemploye.objects.get(serialNumber=n).e_per})
            else:
                mydict_abcde_analyse.update({'e_analyse' : ''})
                mydict_abcde_analyse.update({'e_per' : ''})
            
            mylist_abcde_analyse.append(mydict_abcde_analyse)
    except Exception as ex:
        print('err: %s' %ex)     
    return  mylist_abcde, mylist_abcde_per, mylist_abcde_analyse

def get_jpg_text_name(PATH_IMG, mylist_abcde_analyse, tpl):
    '''
    {'jpg_text_name': [{'title': '员工对分行的技术和工具使员工能够成功地开展工作有何评价？', 
    'a_analyse': 'a00', 'b_analyse': 'b00', 'c_analyse': 'c00', 'd_analyse': 'd00', 
    'e_analyse': 'e00', '0': 'bank/files/img/0.jpg'}, ...]}    
    '''
    jpgs = MyFile(PATH_IMG, ['.jpg']).toNameList()  #图片列表  
    mlist = [dict(m,**{'jpg' : InlineImage(tpl,jpgs[index],width=Mm(180)) })  for (index,m) in enumerate(mylist_abcde_analyse)]    
    return  {'jpg_text_name' : mlist}

def analysis_report(request):    
    """生成分析报告文件 使用word模板   获得 满意度、敬业度、忠诚度  所有统计数据      """   
    user_num = get_user_num()   
    if not user_num:
        meg = '没有答卷  ^o^'
        return render(request, 'bank/excel_import.html', context=locals())
     
    mylist_abcde, mylist_abcde_per, mylist_abcde_analyse = get_title_abcde()
    for (index,mdict) in  enumerate(mylist_abcde):
        if not saveNumImgFile('%s%s.jpeg'%(PATH_IMG,index), list(mdict.keys())[0], list(mdict.values())[0], user_num):
            meg = '保存图片失败。%s%s.jpeg  ^o^' % (PATH_IMG, index)    
            return render(request, 'bank/excel_import.html', context=locals())
    
    for (index,mdict) in  enumerate(mylist_abcde_per):
        if not savePerImgFile('%s%s.jpg'%(PATH_IMG,index), list(mdict.keys())[0], list(mdict.values())[0]):
            meg = '保存图片失败。%s%s.jpg  ^o^' % (PATH_IMG, index)    
            return render(request, 'bank/excel_import.html', context=locals())
    
    
    tpl = DocxTemplate(TPL_FILE)
    jpg_text_name = get_jpg_text_name(PATH_IMG, mylist_abcde_analyse, tpl)    
    context = context_dict(user_num) 
    context.update(jpg_text_name)
    tpl.render(context)
    tpl.save('web/files/AnalysisReport.docx')
    meg = '分析报告文件生成成功  ^o^'
    return render(request, 'bank/excel_import.html', context=locals()) 
    
def get_abcde(switch):
    """ 获得问卷统计 switch=='per' 执行答卷人数、百分比统计； 否则执行答卷人数统计 
    print(get_abcde(''))  返回 类似这样
    [{'员工满意度调查1': [{'e': 6, 'c': 3, 'sum': 30, 'title': '员工对分行的技术和工具使员工能够成功地开展工作有何评价？', 'a': 7, 'b': 6, 'id': 0, 'd': 8}, ... ]},   
     {'员工敬业度调查2': [{'e': 4, 'c': 7, 'sum': 30, 'title': '2员工对分行提供适合员工工作类型的社会信息有何评价？', 'a': 7, 'b': 9, 'id': 0, 'd': 3},     ... ]},    
     {'员工忠诚度调查3': [{'e': 8, 'c': 7, 'sum': 30, 'title': '3员工对总行级信息管理有何评价？', 'a': 5, 'b': 4, 'id': 6, 'd': 6},   ... ]} ]
    
    print(get_abcde('per'))  返回 类似这样
    [{'员工满意度调查1': [{'e': 20.0, 'id': 0, 'title': '员工对分行的技术和工具使员工能够成功地开展工作有何评价？', 'b': 20.0, 'a': 23.33, 'd': 26.67, 'sum': 30, 'c': 10.0}, ... ]},
     {'员工敬业度调查2': [{'e': 13.33, 'id': 0, 'title': '2员工对分行提供适合员工工作类型的社会信息有何评价？', ... ]},
     {'员工忠诚度调查3': [{'e': 26.67, 'id': 6, 'title': '3员工对总行级信息管理有何评价？', 'b': 13.33, 'a': 16.67, 'd': 20.0, 'sum': 30, 'c': 23.33},   ... ]} ]
    """
    titles = get_sort_titles()
    mylist = []
    sum = get_user_num()
    for title in titles:
        mlist = []
        bs = list(Bankemploye.objects.filter(title=title))
        for (id, b) in enumerate(bs):
            if 'per' in switch:
                mlist.append({'id':id,'title':b.investigation,'sum':sum,\
                'a':b.a_per,'b':b.b_per,'c':b.c_per,'d':b.d_per,'e':b.e_per})            
            else:
                mlist.append({'id':id,'title':b.investigation,'sum':sum,\
                'a':b.a,'b':b.b,'c':b.c,'d':b.d,'e':b.e})            
        mylist.append({title:mlist})
    return mylist

def create_excel(request):
    """ 数据统计保存为Excel 1、生成2(4、6)个电子表格文件。2、将2(4、6)个电子表格文件，压缩成一个zip文件。3、下载zip文件  """

    if not get_user_num():
        meg = '没有答卷  ^o^'
        return render(request, 'bank/excel_import.html', context=locals())
    
    all_abcde = get_abcde('')
    all_abcde_per = get_abcde('per')
    if request.method == 'POST':    
        if not os.path.isfile(DOWNLOAD_EXCEL_FILE):
            meg = 'err: %s  ^.o.^' %DOWNLOAD_EXCEL_FILE
            return render(request, 'bank/excel_import.html', context=locals()) 
        return down_file(DOWNLOAD_EXCEL_FILE, os.path.split(DOWNLOAD_EXCEL_FILE)[1])
           
    for i in  range(0,len(all_abcde)):
        title = '%s-%s' %(list(all_abcde[i].keys())[0],'人数')
        listdict =  list(all_abcde[i].values())[0]   
        data = listdictTolists(listdict)
        headings = ['id','title','sum(人数)','A','B','C','D','E']                 
        if not list_to_xlsx(data, headings, '%s%s.xlsx' %(PATH_XLSX, title)):
            meg = 'err: %s list_to_xlsx !  ^.o.^' %title
            return render(request, 'bank/excel_import.html', context=locals()) 

        title = '%s-%s' %(list(all_abcde[i].keys())[0],'百分比')
        listdict =  list(all_abcde_per[i].values())[0]   
        data = listdictTolists(listdict)
        headings = ['id','title','sum(人数)','A %','B %','C %','D %','E %']                 
        if not list_to_xlsx(data, headings, '%s%s.xlsx' %(PATH_XLSX, title)):
            meg = 'err: %s list_to_xlsx !  ^.o.^' %title
            return render(request, 'bank/excel_import.html', context=locals())     
        zipDir(PATH_XLSX, DOWNLOAD_EXCEL_FILE)
    return render(request, 'bank/create_excel.html', context=locals())

def get_sort_serialNumber():
    """获得满意度、敬业度、忠诚度 title 排序开始序号  
    print(get_sort_serialNumber()) [0, 30, 50] 
    """
    titles = set(Bankemploye.objects.values_list('title', flat=True))
    mylist = [int(str(Bankemploye.objects.filter(title=t).first())) for t in titles]
    mylist.sort()
    return mylist

def get_sort_titles():
    """获得满意度、敬业度、忠诚度 排序 title   
    print(get_sort_titles())   ['员工满意度调查1', '员工敬业度调查2', '员工忠诚度调查3']
    """
    return [Bankemploye.objects.get(serialNumber=g).title for g in get_sort_serialNumber()]

def get_start_end_serialNumber(serialNumber):
    """获得开始结束序号    serialNumber：序号 
    print(get_start_end_serialNumber(0))，  获得('员工满意度调查1', 30)    
    print(get_start_end_serialNumber(30))， 获得(员工敬业度调查2, 20)  
    prinr(get_start_end_serialNumber(50))， 获得(忠诚度调查数据3, 20)
    """
    title = Bankemploye.objects.get(serialNumber=serialNumber).title
    count = Bankemploye.objects.filter(title=title).count()
    return title, count

def get_title_Bankemploye(bankemployes):
    """ 获得满意度、敬业度、忠诚度调查数据，返回列表列表
    [['员工满意度调查1', <QuerySet [<Bankemploye: 0>, <Bankemploye: 1>,  ...      ]>],  
     ['员工敬业度调查2', <QuerySet [<Bankemploye: 140>, <Bankemploye: 141>, ...  ]>], 
     ['员工忠诚度调查3', <QuerySet [<Bankemploye: 160>, <Bankemploye: 161>, ...  ]>]]
    
    """    
    mylist = []
    gs = get_sort_serialNumber()
    for g in gs:
        title, count = get_start_end_serialNumber(g)
        mylist.append([title, bankemployes[g : g+count]])
    return mylist

def down_analysisReport(request):
    """下载 分析报告文件"""
    tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files',\
                             'AnalysisReport.docx')
    if not os.path.exists(tpl_path):
        meg = '没有分析报告文件，请选择生成分析报告文件  ^o^'
        return render(request, 'bank/excel_import.html', context=locals())         
    return down_file(tpl_path, 'AnalysisReport.docx')

def help(request, s_name):
    """帮助文档"""    
    if s_name == '(.+)' or s_name == 'menu':
        title_yield = MyFile('bank/static/menu', ['.md']).get_openTxt()
        return render(request, 'bank/help/menu.html', context=locals()) 
        
    meg = ' ^o^'
    return render(request, 'bank/excel_import.html', context=locals())       



def test_questionnaire(request):     
    """模拟答题""" 
    import random
    from bank.models import Bankemploye, Bankuser
    from initdb import roots
    if Bankemploye.objects.all().count() == 0:
        meg = '没有问卷题库 请上传问卷Excel ^o^'
        return render(request, 'bank/excel_import.html', context=locals()) 
    
    if Bankuser.objects.filter(name=request.user.username).count():
        meg = '答卷已经存在, 不允许模拟答题  ^o^'
        return render(request, 'bank/excel_import.html', context=locals())       
    
    user_len = UserInfo.objects.all().count()
    if not user_len:
        meg = '没有用户 请上传用户 ^o^'
        return render(request, 'bank/excel_import.html', context=locals()) 
    
    #Bankuser.objects.all().delete() #删除数据库
    users = UserInfo.objects.values_list('name', flat=True)     
    titles = list(set(Bankemploye.objects.values_list('title', flat=True)))
    for title in titles:
        investigation_list = Bankemploye.objects.filter(title__icontains=title).values_list('investigation', flat=True).order_by('id')          
        for user in users:           
            for i in investigation_list:
                b = Bankuser()
                b.name = user
                b.title = title
                b.ask = i
                b.reply = random.randint(1, 5)
                b.save()
        meg = '%s人模拟答题完成   ^o^' %user_len
                  
    data_statistics()
    return render(request, 'bank/excel_import.html', context=locals())    
    
    
def questionnaire_import(request):
    """上传问卷Excel 问卷电子表格导入数据库(Bankemploye)"""
    if request.method == 'GET':
        return render(request, 'bank/questionnaire_import.html')
    
    Bankemploye.objects.all().delete() #删除数据库
    Bankuser.objects.all().delete() #删除数据库
    if os.path.exists("web/files/AnalysisReport.docx"):
        os.remove("web/files/AnalysisReport.docx") #删除分析报告文件 
        
    """数据库(Bankemploye)字段"""
    k = ['serialNumber', 'title', 'subitem', 'drivingfactors', 'investigation',\
         'classificationNumber', 'score', 'dimensionalItems', 'remarks',\
         'a_analyse', 'b_analyse', 'c_analyse', 'd_analyse', 'e_analyse']
    
    context = {'status': True, 'msg': '上传成功'} \
    if post_excel_model(request, 'questionnaire_excel', Bankemploye, k) \
    else {'status': False, 'msg': '上传失败'}    
    return render(request, 'bank/questionnaire_import.html', context)



def questionnaire_tpl(request):
    """下载问卷模板"""
    tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files', '批量导入问卷模板.xlsx')
    return down_file(tpl_path, 'questionnaire_excel_tpl.xlsx')
   

def inquire_into(request):
    """用户问卷"""
    titles = get_sort_titles()
    title ='、'.join(titles)
    choices = [['1','非常不满意'], ['2','不满意'],['3','一般'],['4','满意'],['5','非常满意']]
    bankemployes = Bankemploye.objects.filter()
    title_Bankemployes = get_title_Bankemploye(bankemployes) 
    name = request.user.username
    if request.method == 'POST':
        if Bankuser.objects.filter(name = name):
            meg = '历史提交'
        else:
            cleanData = request.POST.dict()
            del cleanData['csrfmiddlewaretoken']        
            
            if len(set(cleanData.values())) == 1:
                meg = '答卷不允许全部只选【%s】, 请重新答卷 ^o^' % dict12345[list(set(cleanData.values()))[0]]
                return render(request, 'bank/excel_import.html', context=locals()) 
            
            for index,(k,v) in enumerate(cleanData.items()):
                b = Bankuser()          
                b.name = name
                b.title = request.POST.get('title','')
                b.ask = k
                b.reply = int(v)
                b.title = Bankemploye.objects.get(serialNumber=index).title    
                b.save()
            data_statistics()
            meg = '刚刚提交'
        title = '%s %s总评结果'%(name, title)
        data, overallAppraisal = user_data_per(name)             
        return render(request, 'bank/user_sum.html', context=locals())       
    if bankemployes.count() == 0:
        meg = '没有问卷题库 请上传问卷Excel ^o^'
        return render(request, 'bank/excel_import.html', context=locals())    

    return render(request, 'bank/inquire_into.html', context=locals())

def set_evaluation_criteria(sum, total):
    '''设置评估标准'''
    b = float(sum)*100/float(total)  
    return b >= 90 and '非常满意' or b >= 80 and '满意' or b >= 60 and '一般' \
        or b >= 40 and '不满意' or '非常不满意'

def get_user_num():
    '''获得问卷人数，返回整数。 30 ''' 
    try:
        name = Bankuser.objects.get(id=1).name 
        return int(Bankuser.objects.filter().count()/Bankuser.objects.filter(name=name).count())
    except Exception as ex:
        print('err: %s' %ex) 
        return 0
    
def overall_evaluation(request):
    '''总体评价 可视化图形'''
    title = '、'.join(get_sort_titles())
    user_num = get_user_num()
    if not user_num:
        meg = '没有答卷 ^o^'
        return render(request, 'bank/excel_import.html', context=locals())
    reply_list = Bankuser.objects.values_list('reply', flat=True)
    reply_sum = int(sum(reply_list)) #<class 'numpy.int64'>  --> <class 'int'>
    total = Bankemploye.objects.filter().count() * user_num * 5           
    title = '%s 总评结果'% title
    overallAppraisal = set_evaluation_criteria(reply_sum, total)
    name = '得分: %s\n占比: %.2f%%'%(reply_sum,float(reply_sum)*100/total)
    d = [{"value" : reply_sum, "name" : name},\
        {"value" : total, "name":"总分: %s" %total},\
        {"value" : user_num, "name":"问卷人数: %s" %user_num}]
    data = json.dumps(d) 
    return render(request, 'bank/overall_evaluation.html', context=locals())


def get_reply_list(title):
    ''' 获得所有 调查问题项 问卷结果统计 返回列表列表 
    id 号     [     1,             2,            3,             4,           ...        140      ]           
    返回平均值 [['5','4','4'], ['1','3','2'], ['2','3','4'], ['5','1','2']],    ...  ['3','3','3']]
    '''
    investigation_list = Bankemploye.objects.filter(title__icontains=title).values_list('investigation', flat=True).order_by('id')
    ask_num = len(investigation_list)
    mylist = []
    for (index,i) in enumerate(investigation_list):
        mlist = []
        count = Bankuser.objects.filter(ask=i).count()
        if count == 0:
            return ''
        else:
            for b in range(0, count):
                mlist.append(Bankuser.objects.get(id=b*ask_num+index+1).reply)
            mylist.append(mlist)
    return mylist



def get_all_user_per(request, investigation_list, ask_num):
    ''' 获得所有 调查问题项 问卷平均得分 返回列表
        id 号               [ 1,  2,  3,  4  ...   ]           
        investigation_list ['员工对分行的技术和工具使员工能够成功地开展工作有何评价?',
        '员工对能够及时获得足够有效的信息以有效地完成工作有何评价？' ... '员工就其工作对分行工会负责人有何评价？']
        返回平均值           [ '2.67','1.36','3.53','5.00',  ... '4.35' ]'''
    mylist = []
    for (index,investigation) in enumerate(investigation_list):
        s = sum(Bankemploye.objects.filter(investigation=investigation).values_list('a', flat=True))*1 +\
        sum(Bankemploye.objects.filter(investigation=investigation).values_list('b', flat=True))*2 +\
        sum(Bankemploye.objects.filter(investigation=investigation).values_list('c', flat=True))*3 +\
        sum(Bankemploye.objects.filter(investigation=investigation).values_list('d', flat=True))*4 +\
        sum(Bankemploye.objects.filter(investigation=investigation).values_list('e', flat=True))*5
        s_per = str(Decimal(str(s*1.0/(ask_num*1.0))).quantize(Decimal('0.00')))

        mylist.append(s_per)
    return mylist

    
def user_questionnaire(request, s_name):
    '''问卷查询  柱状可视化图形 '''
    user_num = get_user_num()
    if not user_num:
        meg = '没有答卷 ^o^'
        return render(request, 'bank/excel_import.html', context=locals())

    if s_name == '(.+)':
        name_list = list(set(Bankuser.objects.values_list('name', flat=True))) 
        name_list.sort()
        
        choices = {'a':'A - 非常不满意', 'b':'B - 不满意','c':'C - 一般','d':'D - 满意','e':'E - 非常满意'}
        
        titles = get_sort_titles()
        title_choices = dict(zip(range(1,len(titles)+1),titles))
        title = '、'.join(titles)
        
        #5分法与得分百分比复合查询
        abcde_choices = {'a_per':'A - 非常不满意', 'b_per':'B - 不满意','c_per':'C - 一般','d_per':'D - 满意','e_per':'E - 非常满意'}
        l = range(1,100)
        per_choices = dict(zip(l,['%s%%'%i for i in l]))
        
        name = request.POST.get('name','')
        abcde = request.POST.get('abcde','')
        title_str = request.POST.get('title','')
        abcde_5 = request.POST.get('abcde_5','')
        per = request.POST.get('per','')
                
        if not name.strip() and not abcde.strip() and not title_str.strip()\
            and not per.strip():
            return render(request, 'bank/user_questionnaire.html', context=locals()) 
        title = '%s %s' %(name.strip(),title) 
        #按用户查询
        if name: 
            reply_list = Bankuser.objects.filter(name=name).values_list('reply', flat=True).order_by('id')
            Bankuser_list = Bankuser.objects.filter(name=name).order_by('id')  

            dataX = json.dumps(list(range(0, len(reply_list))))
            data = json.dumps(list(reply_list))
            return render(request, 'bank/user_question.html', context=locals())
         
        #按按五分法查询
        elif abcde: 
            x_y_meg = '<h4>【 %s 】统计结果</h4>一、柱状图显示<br>X轴-问卷题序号 Y轴-答卷人数, 最后最高的是答卷总人数' %(choices.get(abcde))                            
            banks = Bankemploye.objects.filter().order_by('id')    
            if 'a' in abcde: b = banks.values_list('a', flat=True)
            if 'b' in abcde: b = banks.values_list('b', flat=True)
            if 'c' in abcde: b = banks.values_list('c', flat=True)
            if 'd' in abcde: b = banks.values_list('d', flat=True)
            if 'e' in abcde: b = banks.values_list('e', flat=True)
            l = len(b)
            datax = list(range(0, l+1))
            data = list(b)
            data.insert(l, user_num)
            dataX = json.dumps(datax)
            data = json.dumps(data) 
                       
            name = '人数'
            return render(request, 'bank/all_investigation.html', context=locals())
        
        #按满意度敬业度忠诚度查询
        elif title_str:
            title = title_choices.get(int(title_str))
            x_y_meg = '<h4>统计结果</h4>一、柱状图显示<br>X轴-问卷题序号 Y轴-得分(最后显示的是采用5分制评分标准)'                                  
            investigation_list = Bankemploye.objects.filter(title=title).values_list('investigation', flat=True).order_by('id')
            dataX, data = x_y_data(request, investigation_list, user_num)    
            banks = Bankemploye.objects.filter(title=title).all()
            return render(request, 'bank/all_investigation.html', context=locals())        

        #5分法与得分百分比复合查询
        elif per:
            banks = Bankemploye.objects.filter()  
            if abcde_5 == 'a_per':
                banks = Bankemploye.objects.filter(a_per__gte=per)
                b = banks.values_list('a', flat=True).order_by('id')   
            elif abcde_5 == 'b_per':
                banks = Bankemploye.objects.filter(b_per__gte=per) 
                b = banks.values_list('b', flat=True).order_by('id') 
            elif abcde_5 == 'c_per':
                banks = Bankemploye.objects.filter(c_per__gte=per)   
                b = banks.values_list('c', flat=True).order_by('id') 
            elif abcde_5 == 'd_per':
                banks = Bankemploye.objects.filter(d_per__gte=per)   
                b = banks.values_list('d', flat=True).order_by('id') 
            else:
                banks = Bankemploye.objects.filter(e_per__gte=per)  
                b = banks.values_list('e', flat=True).order_by('id') 
            x_y_meg = '<h4>【 %s >= %s 】复合查询结果</h4>一、柱状图显示<br>X轴-问卷题序号 Y轴-答卷人数, 最高的是答卷总人数' %(abcde_choices.get(abcde_5), per_choices.get(int(per)))                                            
            l = len(b)
            datax = list(range(0, l+1))
            dataX = json.dumps(datax)
            data = list(b)
            data.insert(l, user_num)                
            data =  json.dumps(data)
            name = '人数'                                     
            return render(request, 'bank/all_investigation.html', context=locals())        
                   
        else:
            print('==========')
            pass
    meg = '访问地址错误 ^o^'
    return render(request, 'bank/excel_import.html', context=locals())


def x_y_data(request, investigation_list, user_num):
    l = len(investigation_list)
    data = get_all_user_per(request, investigation_list, user_num)
    data.insert(l, '5')        
    return json.dumps(list(range(0, l+1))) , json.dumps(data)           
    
def all_investigation(request):
    '''问卷图表显示 所有问卷结果 调查问题项  柱状可视化图形'''
    title = '、'.join(get_sort_titles())
    x_y_meg = '<h4>【 全部问卷 】统计结果</h4>一、柱状图显示<br>X轴-问卷题序号 Y轴-得分(最后显示的是采用5分制评分标准)'                      
    investigation_list = Bankemploye.objects.filter().values_list('investigation', flat=True).order_by('id')
    if not investigation_list:
        meg = '没有问卷题库 ^o^'
        return render(request, 'bank/excel_import.html', context=locals())
    user_num = get_user_num()    
    if not user_num:
        meg = '没有答卷 ^o^'
        return render(request, 'bank/excel_import.html', context=locals())     
    dataX, data = x_y_data(request, investigation_list, user_num)    
    banks = Bankemploye.objects.filter().all()
    name = '平均得分'  
    return render(request, 'bank/all_investigation.html', context=locals())

def all_investigationRanking(request):
    '''问卷图表显示排名  问卷结果排名 柱状可视化图形'''   
    title = ' '.join(get_sort_titles())    
    x_y_meg = '<h4>【 全部问卷 】统计结果</h4>一、柱状图显示<br>X轴-问卷题序号 Y轴-得分(最后显示的是采用5分制评分标准)'                      
    investigation_list = Bankemploye.objects.values_list('investigation', flat=True).order_by('id') 
    user_num = get_user_num()
    if not user_num:
        meg = '没有答卷 ^o^'
        return render(request, 'bank/excel_import.html', context=locals())
    
    l = len(investigation_list)
    v = get_all_user_per(request, investigation_list, user_num)         
    d = dict(zip(investigation_list,v))     
    mylist = dict_sorted(d)
    x_list = [i for (i,k) in enumerate(mylist)]    
    y_list = [k[1] for k in mylist]
    x_list.insert(l, l)
    y_list.insert(l, '5')
    title =  '%s %s个问卷问题 平均得分排名结果'%(title, l)
    dataX = json.dumps(x_list)
    data = json.dumps(y_list)                   
    ks = [k[0] for k in mylist]
    bankemployes =[Bankemploye.objects.filter(investigation=k)  for k in ks]    
    name = '平均得分'  
    return render(request, 'bank/all_investigationRanking.html', context=locals())

def user_data_per(name):
    '''问卷人 平均得分'''
    reply_list = Bankuser.objects.filter(name=name).values_list('reply', flat=True) 
    
    total = len(reply_list)
    if not total: 
        return '', ''  
    sum = get_sum(reply_list) 

    overallAppraisal = set_evaluation_criteria(sum, total*5)
    per = '%.2f' %(float(sum)*100/total/5.0)
    data = [{'value': per, 'name': '%s/%s' %(int(float(sum)) , total*5)}] 
    
    return json.dumps(data), overallAppraisal      

def contactus(request):
    if request.method != 'POST':
        return render(request, 'bank/contactus.html', context=locals())
    
    meg = '提交成功，我们将在24小时内联系您 ^o^'
    cleanData = request.POST.dict() 
    del cleanData['csrfmiddlewaretoken']       
    iscontact = Contacts.objects.filter(content = cleanData.get('content',''))
    if iscontact:
        meg = '已经提交过了，不要重复提交！我们将在24小时内联系您 ^o^'
    else:            
        c = Contacts(**cleanData)
        c.save()            
    return render(request, 'bank/excel_import.html', context=locals())

def upload(request):
    '''上传文件'''  
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
    """下载文件"""
    tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files',\
                             'AnalysisReport.docx')
    tpl_path = TPL_FILE
    if not os.path.exists(tpl_path):
        meg = '%s 文件不存在。  ^o^' %tpl_path
        return render(request, 'bank/excel_import.html', context=locals())         
    return down_file(tpl_path, 'tpl_word.docx')
