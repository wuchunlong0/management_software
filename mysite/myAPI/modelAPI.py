# -*- coding: utf-8 -*-
# 测试：http://localhost:8888/mytest/get_id/

from __future__ import unicode_literals
import os,tempfile, datetime, uuid
from myAPI.listdictAPI import get_dict_val
from myAPI.listAPI import pinyin

# 返回 <class 'int'>
def get_model_first_id(model):
    """ 获得数据库第一条记录的id"""
    if model.filter().count() == 0:
        return 0
    return model.filter().first().id

def get_model_last_id(model):
    """ 获得数据库最后一条记录的id"""    
    if model.filter().count() == 0:
        return 0
    return model.filter().last().id
    
def get_model_up_id(model, id):
    """ 获得数据库上一条记录的id。当数据库做删除操作后，id是不连续的。设定：只有一条记录时，上一条记录的id=0
        id   name
        1
        2
        5         #当前记录id=5;  上一条记录id=2     
    """
    try:
        if model.filter().count() == 1: 
            return 0
        else:    
            return  model.filter(id__lt=id).order_by("-id").first().id  
    except Exception as ex:
        print(str(ex))
        return 0

def get_model_name_up_id(model,name,id):
    """ 获得数据库name,id上一条记录的id。当数据库做删除操作后，id是不连续的。
        id     name   ...
        1       wu
        2       wu
        4       zh
        5       wu   #当前记录name=wu  id=5;  上一条记录  name=wu  id=2     
    """
    try:
        if model.filter().count() == 1: 
            return 0
        else:   
            return  model.filter(name = name, id__lt=id).order_by("-id").first().id  
    except Exception as ex:
        print(str(ex))
        return 0

"""
model.objects.values()能够以列表字典形式，获得数据库字段值，字段有外键时，只能获得:字段_id
 该函数以列表字典形式，获得数据库字段值，也可以获得外键字段值。
 models_values数据库列表字典形式:[{'字段1':'1','字段2':'2',...},{'字段1':'11','字段2':'22',...}, ...]
 listdict=[{'字段名': 外键数据库名}, ...]。例如Account项目 外键：[dict(author=User),dict(company=Company),dict(material=Material)]
 测试在：http://localhost:8888/test/uikit_page2/
 def get_model_values(models_values,listdict):    
     try:                                     
         for T in models_values:
             adddict = {}                         
             for k,v in T.items():
                 for (index,d) in enumerate(listdict):                                        
                     if k == list(d)[0] + '_id':
                         adddict.update({list(d)[0] : str(list(d.values())[0].objects.get(id=v)) }) if v else adddict.update({list(d)[0] :v})                                                      
                         if index == 0:
                             adddict.update(T)
             yield adddict 
                                                                                                                        
     except Exception as ex:
         print("get_model_listdict() err!"  + str(ex))
         yield  {}
"""
# 与上面的功能是一样的
def get_model_values(models_values,listdict):    
    try:                                     
        for T in models_values:
            adddict = {}                         
            for k,v in T.items():
                for (index,d) in enumerate(listdict):                                        
                    for k1,v1 in d.items():
                        if k == k1 + '_id':
                            adddict.update({k1 : str(v1.objects.get(id=v)) }) if v else adddict.update({k1 :v})                                                      
                            if index == 0:
                                adddict.update(T)
            yield adddict 
                                                                                                                       
    except Exception as ex:
        print("get_model_listdict() err!"  + str(ex))
        yield  {}

#外键 由列表中某个元素获得下标。数据库名model，值value  测试：http://localhost:8888/accountTest/str_get_id/
def get_model_id(model,field,value):
    models = list(model.objects.values_list(field,flat=True)) #列表
    print('models===',models)
    try:
        
        id = models.index(value) 
    except Exception as ex:
        id = 0
        print('#####')
        
    return  id#返回列表中某个元素的下标

def _filter(model, cleanData):
    """ name、date_start、date_end 过滤 """
    model = model.filter().order_by("-id")
    name, date_start, date_end = '','',''
    if cleanData.get('name', '') :
        name = cleanData['name']
    if cleanData.get('name_in', ''):
        name = cleanData['name_in']

    if cleanData.get('date_start', ''):
        date_start = cleanData['date_start']
    if cleanData.get('date_end', ''):
        date_end = cleanData['date_end']
        

    if not name and not date_start and date_end:      #001
        model = model.filter(date__lte = date_end)  

    if not name and date_start and not date_end:      #010
        model = model.filter(date__gte = date_start)      
    
    if not name and date_start and date_end:          #011
        model = model.filter(date__gte = date_start, \
                             date__lte = date_end)  
   
    if name and not date_start and not date_end:      #100
        model = model.filter(name__icontains = name)  

    if name and not date_start and date_end:          #101
        model = model.filter(name__icontains = name, \
                             date__lte = date_end)  

    if name and date_start and not date_end:          #110
        model = model.filter(name__icontains = name, \
                             date__gte = date_start)  
    
    if name and date_start and date_end:             #111
        model = model.filter(name__icontains = name, \
                         date__gte = date_start, \
                         date__lte = date_end )  
    return model

def _filter_name_customer(model, cleanData):
    """ name、customer、date_start、date_end 过滤 """
    model = model.filter().order_by("-id")
    name, customer, date_start, date_end = '','','',''
    if cleanData.get('name', '') :
        name = cleanData['name']
    if cleanData.get('name_in', ''):
        name = cleanData['name_in']
    if cleanData.get('customer', '') :
        customer = cleanData['customer']
    if cleanData.get('customer_in', ''):
        customer = cleanData['customer_in']
    if cleanData.get('date_start', ''):
        date_start = cleanData['date_start']
    if cleanData.get('date_end', ''):
        date_end = cleanData['date_end']
        
    if not name and not customer and not date_start and date_end:      #0001
        model = model.filter(date__lte = date_end)  

    if not name and not customer and date_start and not date_end:      #0010
        model = model.filter(date__gte = date_start)      
    
    if not name and not customer and date_start and date_end:          #0011
        model = model.filter(date__gte = date_start, \
                             date__lte = date_end)  
   
    if not name and customer and not date_start and not date_end:      #0100
        model = model.filter(customer__icontains = customer)  

    if not name and customer and not date_start and date_end:          #0101
        model = model.filter(customer__icontains = customer, \
                             date__lte = date_end)  

    if not name and customer and date_start and not date_end:          #0110
        model = model.filter(customer__icontains = customer, \
                             date__gte = date_start)  
    
    if not name and customer and date_start and date_end:             #0111
        model = model.filter(customer__icontains = customer, \
                         date__gte = date_start, \
                         date__lte = date_end )  

    if name and not customer and not date_start and not date_end:     #1000
        model = model.filter(name__icontains = name)  

    if name and not customer and not date_start and date_end:     #1001
        model = model.filter(name__icontains = name, \
                             date__lte = date_end )  
    
    if name and not customer and date_start and not date_end:     #1010
        model = model.filter(name__icontains = name, \
                             date__gte = date_start)  
    
    if name and not customer and date_start and date_end:     #1011
        model = model.filter(name__icontains = name, \
                             date__gte = date_start,\
                             date__lte = date_end )  
    
    if name and customer and not date_start and not date_end:     #1100
        model = model.filter(name__icontains = name, \
                             customer__icontains = customer)  
    
    if name and customer and not date_start and date_end:     #1101
        model = model.filter(name__icontains = name, \
                             customer__icontains = customer,\
                             date__lte = date_end ) 

    if name and customer and date_start and not date_end:     #1110
        model = model.filter(name__icontains = name, \
                             customer__icontains = customer,\
                             date__gte = date_start) 

    if name and customer and date_start and date_end:     #1111
        model = model.filter(name__icontains = name, \
                             customer__icontains = customer,\
                             date__gte = date_start,\
                             date__lte = date_end ) 
    return model

def get_model_data(model, cleanData):
    name_list = list(set(model.values_list('name', flat=True)))    
    name_list = pinyin(name_list)
    name = get_dict_val(cleanData)
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()])        
    datas = _filter(model, cleanData)
    return name, name_list, queryString, datas

def get_model_name_customer(model, cleanData):
    name_list = list(set(model.values_list('name', flat=True)))
    name_list = pinyin(name_list)
    name = get_dict_val(cleanData)
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()])        
    datas = _filter_name_customer(model, cleanData)
    return name, name_list, queryString, datas

def get_post_data(request, model):
    cleanData = request.GET.dict() 
    if request.method == 'POST':
        cleanData = request.POST.dict() 
        dict.pop(cleanData,'csrfmiddlewaretoken')
    page = int(cleanData.get('page', 1))
    name, name_list, queryString, datas = get_model_name_customer(model, cleanData)     
    fileName = r'xlsx-%s.xlsx' % (datetime.datetime.now().strftime('%Y%m%d'),) #下载文件名
    tempFilePath = os.path.join(tempfile.mkdtemp(), 'online-%s' % uuid.uuid4().hex) #保存电子表格 含路径文件名    
    return datas, tempFilePath, fileName
