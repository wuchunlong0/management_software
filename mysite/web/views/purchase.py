# -*- coding: utf-8 -*-
# 采购模块
import os
import xlrd
from django.conf import settings
from django.shortcuts import render, redirect
from web import models
from web.forms.purchase import PurchaseForm
from myAPI.downfileAPI import down_file
from myAPI.pageAPI import djangoPage, PAGE_NUM
from myAPI.modelAPI import get_model_first_id, get_model_last_id, \
                    get_model_up_id, get_model_name_up_id, get_model_data
                            

from myAPI.excelAPI import get_date
from decimal import * #浮点数保留2位小数

def purchase_id_update(request, model, id):
    """" 更新金额 更新结余款 """
    id = int(id)
    model.filter(id=id).update(operator = request.user.username)  #更新经办人为登录用户    
    #更新数据库第一条记录  备注 = '结余'
    if id == get_model_first_id(model):
        model.filter(id=id).update(note = '结余')  #更新备注    
    money = round(model.get(id=id).number * model.get(id=id).price, 2) #金额保留2位小数
    model.filter(id=id).update(money = money)  #更新金额        
    if model.get(id=id).note != '结余' : # 备注 ！= '结余'，更新结余款
        name = model.get(id=id).name
        up_id = get_model_name_up_id(model,name,id)
        if up_id:
            balance_1 = model.get(id=up_id).balance  #上一条        
            balance = round(balance_1 + model.get(id=id).money - model.get(id=id).payment, 2)
            model.filter(id=id).update(balance = balance)  #更新结余款
    return ''

def purchase_list(request, page):
    """采购列表"""
    cleanData = request.GET.dict()          
    model = models.Purchase.objects
    if request.method == 'POST':
        page = 1
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken') #删除字典中的键'csrfmiddlewaretoken'和值
   

    name, name_list, queryString, datas = get_model_data(model, cleanData)
     
    moneys = round(sum(datas.filter().values_list('money', flat=True)), 2) #金额总和    
    payments = round(sum(datas.filter().values_list('payment', flat=True)), 2)  #支付款总和
    if datas:
        balance =  datas.filter().get(id=get_model_first_id(datas)).balance #结余款 最后一条记录(-id第一条记录)        
    data_list, pageList, num_pages, page = djangoPage(datas,page,PAGE_NUM)  #调用分页函数
    offset = PAGE_NUM * (page - 1) 
    return render(request, 'web/purchase/purchase_list.html', context=locals())

    
def purchase_add(request):
    """添加采购"""
    if request.method == 'GET':
        name_list = set(models.Purchase.objects.values_list('name', flat=True))  # 送货产品名称
        product_list = set(models.Purchase.objects.values_list('product', flat=True))  #采购产品名称
        return render(request, 'web/purchase/purchase_add.html', context=locals())
    cleanData = request.POST.dict() #POST对象直接转为字典
    dict.pop(cleanData,'csrfmiddlewaretoken') #删除字典中的键'csrfmiddlewaretoken'和值
    models.Purchase(**cleanData).save()
    # 更新数据库记录
    model = models.Purchase.objects
    purchase_id_update(request, model, get_model_last_id(model))
    return redirect('/web/purchase/list/(.+)')
 
def purchase_edit(request, cid):
    """编辑采购"""
    obj = models.Purchase.objects.get(id=cid)
    if request.method == 'GET':
        return render(request, 'web/purchase/purchase_edit.html', context=locals())
    form = PurchaseForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        # 更新数据库记录
        model = models.Purchase.objects
        purchase_id_update(request, model, cid)
        return redirect('/web/purchase/list/(.+)')
    return render(request, 'web/purchase/purchase_edit.html', context=locals())
 
def purchase_del(request, cid):
    """删除采购"""
    model = models.Purchase.objects
    name = model.get(id=cid).name
    model.filter(id=cid).delete()
    ids = model.filter(name=name).values_list('id', flat=True)        
    for id in ids:
        purchase_id_update(request, model, id)                
    return redirect('/web/purchase/list/(.+)')

def post_excel_model_purchase(request, post_file_excel, model, k):
    ''' Excel文件，多张工作表（数据），导入到数据库
        post_file_excel: 前端上传的文件名
        model:  数据库
        K: 数据库字段, 与Excel表格列对应    
    '''
    file_excel = request.FILES.get(post_file_excel)
    ext = os.path.splitext(file_excel.name)[1]    
    if 'xls' not in ext and 'xlsx' not in ext:
        return 'err: 文件格式错误，请上传Excel文件。'         
    model.objects.all().delete() #删除数据库     
    workbook = xlrd.open_workbook(file_contents=file_excel.file.read())
    sheet_sum = len(workbook.sheet_names())  # 获取电子表格 工作表总数
    for index in range(0, sheet_sum):
        ret = excel_sheet_index_purchase(workbook, model, k, index)
        if ret[0:3] == 'err':
            return ret
    return str(sheet_sum)

def excel_sheet_index_purchase(workbook, model, k, index_n):
    """Excel文件(单元格合并的电子表格同样适用)，导入数据库
    打开上传的Excel文件
    file_excel = request.FILES.get(post_file_excel)
    workbook = xlrd.open_workbook(file_contents=file_excel.file.read())  
    
    打开本地Excel文件
    workbook = xlrd.open_workbook(filename='本地文件路径.xlsx')      
    model:  数据库
    K: 数据库字段, 与Excel表格列对应
    index_n: 工作表序号    
    """
    row_num = 0
    ret = "ok"
    sheet = workbook.sheet_by_index(index_n)      
    try:
        mylist = []
        object_list = []
        v7 = 0
        for row_num in range(1, sheet.nrows):  #sheet.nrows -- 电子表格总行数；row_num -- 从第1行开始读；电子表格默认从0行开始。
            row = sheet.row(row_num) #row -- [empty:'', empty:'', text:'HZ-616S（高）', number:10000.0, number:7.8, number:78000.0, empty:'', number:1794459.1, empty:'', empty:'']           
            v = []
            for (index,r) in enumerate(row): #一次处理电子表格一行             
                s = r.value               
                if s:
                    if isinstance(s, str):
                        if row_num == 1 and index == 10:   #电子表格第1行
                            v.append('结余')
                        else:
                            v.append(s.strip())  
                    else:
                        if index == 0:
                            v.append(get_date(s)) #日期转换 43250 --> 2018-05-30
                        elif row_num == 1 and index == 10:   #电子表格第1行
                            v.append('结余')                       
                        else:
                            v.append(str(Decimal(s).quantize(Decimal('0.00')))) #浮点数保留2位小数
                else:                                           
                    if row_num == 1:   #电子表格第1行 空
                        if index == 3 or index == 4 or index == 5 or index == 6 or index == 7: #index类似电子表格一行中的A1、B1、C1、D1 ...
                            v.append(0)
                        elif index == 0:
                            v.append(get_date(61)) # 61 --> 1900-03-01                                               
                        elif index == 10:
                            v.append('结余')  #电子表格第1行 备注空，则设定为结余
                        else:
                            v.append('')
                    else: 
                        if index == 0 or index == 1 or index == 9:  #合并单元格 操作
                            v.append(mylist[row_num-2][index])
                        else:
                            if index == 2 or index == 8 or index == 10: 
                                v.append('')
                            else:
                                v.append(0)
            
            v[5] = round(float(v[4]) * float(v[3]), 2) #金额 = 单价 * 数量 
            if row_num != 1:   #不是电子表格第1行
                v[7]  =  round(v7 + v[5] - float(v[6]), 2)  
                v7 = v[7]            
            mylist.append(v)
            d = dict(zip(k,v)) 
            object_list.append(model(**d))                 
        model.objects.bulk_create(object_list, batch_size=20)                                
    except Exception as e:
        ret =  'err: %s。 工作表:%s;  %s行: %s。' %(e, index_n+1, row_num+1, v)
    return ret


def purchase_import(request):
    """批量导入 采购数据"""
    if request.method == 'GET':
        return render(request, 'web/purchase/purchase_import.html')         
    k = ['date','name', 'product', 'number', 'price', 'money', 'payment', 'balance', 'payment_method','operator', 'note']
    ret = post_excel_model_purchase(request, 'post_file_excel', models.Purchase, k) 
    if ret[0:3] == 'err':
        context = {'status': False, 'msg': '导入失败! %s' %ret}
    else:
        model = models.Purchase.objects
        ids = model.values_list('id', flat=True)        
        for id in ids:
            purchase_id_update(request, model, id)            
        context = {'status': True, 'msg': '导入成功! 导入了%s张工作表. ' %ret}     
    return render(request, 'web/purchase/purchase_import.html', context)

def purchase_tpl(request):
    """下载采购模板"""
    tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files', '批量导入采购模板.xlsx')
    return down_file(tpl_path, 'purchase_excel_tpl.xlsx')


    
