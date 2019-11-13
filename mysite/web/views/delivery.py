# -*- coding: utf-8 -*-
# 送货模块
import os
import xlrd
import tempfile, datetime, uuid
from myAPI.excelAPI import get_date
from myAPI.downfileAPI import down_file
from myAPI.pageAPI import djangoPage, PAGE_NUM
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect, HttpResponse,\
    StreamingHttpResponse
from web.forms.delivery import DeliveryForm
from web.models import Delivery, Deliverycustomer, Deliveryproduct
from myAPI.modelAPI import get_model_first_id, get_model_last_id, \
                            get_model_up_id, get_model_name_up_id,\
                            get_model_data, get_model_name_customer, get_post_data
from myAPI.listAPI import pinyin
from myAPI.listdictAPI import get_dict_customer
from myAPI.excelAPI import list_to_xlsx
from myAPI.fileAPI import downfile

def convertxlsx(data_list, filePath, ids):
    ret = True
    try:
        # 数据库字段值，转化为电子表格值。 电子表格标题栏。1、与数据库字段保持一致。
        headings = ['序号','采购日期','送货单位','送货单号码','客户名称','送货产品名称','数量',\
                    '单价','金额','经办人','备注']

        dates = [str(i.date + datetime.timedelta(hours=8)).split('+')[0] for i in data_list] #采购日期+时差                      
        names = [i.name for i in data_list] #送货单位                                  
        nums = [i.num for i in data_list] #送货单号码        
        customer = [i.customer for i in data_list ] #客户名称        
        product = [i.product for i in data_list ] #送货产品名称        
        number = [i.number for i in data_list ] #数量
        price = [i.price for i in data_list ] #单价       
        money = [i.money for i in data_list ] #金额
        operator = [i.operator for i in data_list ] #经办人       
        note = [i.note for i in data_list ] #备注
        
        data = [ids, dates, names, nums, customer, product, number, \
            price, money, operator, note, ]
        if not list_to_xlsx(data, headings, filePath): # 保存为电子表格
            ret = False
    except Exception as _e:
        ret = False
    return ret

#单页保存Excel
def makexlsx_page(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Delivery.objects)
    datas, pageList, num_pages, page = djangoPage(datas, page, PAGE_NUM)  #调用分页函数
    ids = [i+PAGE_NUM * (page - 1) for i in range(1,PAGE_NUM+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return downfile(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/delivery/list/%s' % (page))

#全部保存Excel
def makexlsx_all(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Delivery.objects)
    ids = [i for i in range(1,len(datas)+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return downfile(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/delivery/list/%s' % (page))

def delivery_list(request, page):
    """送货列表"""
    cleanData = request.GET.dict()          
    model = Delivery.objects
    if request.method == 'POST':
        page = 1
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken') 
        
    name, name_list, queryString, datas = get_model_name_customer(model, cleanData)
    customer_list = list(set(Deliverycustomer.objects.values_list('name', flat=True))) # 客户名称    
    customer_list = pinyin(customer_list)
    customer = get_dict_customer(cleanData)
    moneys = round(sum(datas.filter().values_list('money', flat=True)), 2) #金额总和          
    data_list, pageList, num_pages, page = djangoPage(datas,page,PAGE_NUM)  #调用分页函数
    offset = PAGE_NUM * (page - 1) 
    return render(request, 'web/delivery/delivery_list.html', context=locals())


def delivery_add(request):
    """添加送货"""
    if request.method == 'GET':
        name_list = ['辙炜送货','俊途送货','琛亚送货','国程送货']
        customer_list = set(Deliverycustomer.objects.values_list('name', flat=True)) # 客户名称
        product_list = set(Deliveryproduct.objects.values_list('name', flat=True))   # 送货产品名称
        return render(request, 'web/delivery/delivery_add.html', context=locals())
    cleanData = request.POST.dict() 
    dict.pop(cleanData,'csrfmiddlewaretoken') 
    Delivery(**cleanData).save()
    return redirect('/web/delivery/list/(.+)')

def delivery_edit(request, cid):
    """编辑送货"""
    obj = Delivery.objects.get(id=cid)
    if request.method == 'GET':
        form = DeliveryForm(instance=obj)
        return render(request, 'web/delivery/delivery_edit.html', context=locals())
    form = DeliveryForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        # 更新数据库记录        
        money = round(Delivery.objects.get(id=cid).number * Delivery.objects.get(id=cid).price, 2) #金额保留2位小数
        Delivery.objects.filter(id=cid).update(money = money)  #更新金额 
        Delivery.objects.filter(id=cid).update(operator = request.user.username)  #更新经办人为登录用户   
        return redirect('/web/delivery/list/(.+)')
    return render(request, 'web/delivery/delivery_edit.html', context=locals())

def delivery_del(request, cid):
    """删除送货"""
    Delivery.objects.filter(id=cid).delete()
    return redirect('/web/delivery/list/(.+)')


def post_excel_model_finance(request, post_file_excel, model, k):
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
        ret = workbook_finance(workbook, 0, index, model, k) #从电子表格0行开始
        if ret[0:3] == 'err':
            return ret
    return str(sheet_sum)

def workbook_finance(workbook, x, index, model, k):
    """ 电子表格，多张工作表写入数据库
        workbook: workbook = xlrd.open_workbook(file_contents=file_excel.file.read())
        x: 从x行开始  x=0,1,2...
        index: 工作表序号
        model: 数据库
        K: 数据库字段, 与Excel表格列对应         
    """
    sheet = workbook.sheet_by_index(index)  
    try:
        #1.1、电子表格转换为列表
        mylist = []
        for row_num in range(x, sheet.nrows): #从x行开始  x=0,1,2...
            row = sheet.row(row_num) #row -- [empty:'', empty:'', text:'HZ-616S', number:10000.0]           
            v = []
            for r in row: #一次处理电子表格一行                           
                v.append(r.value)
            mylist.append(v)

        #2.1、列表中清除空格行 和 以‘日期’开头的行；2、插入送货单位名称、经办人
        mlist = []
        name = ''
        for v in mylist:    
            if any(v) and v[0] != '日期': #列表中清除空格行 和 以‘日期’开头的行
                if isinstance(v[0], str):
                    name = v[0] #获得送货单位名称；字符串开始行的第一个单元格值。
                else:
                    v.insert(1,name) #插入 送货单位名称
                    v.insert(8,'李小明')  #插入 经办人
                    mlist.append(v)
                                 
        #3.1、列表数据，初始化成与数据库字段一样的数据类型；2、数据写入数据库 
        object_list = []      
        for v in mlist:
            v[0] =  get_date(int(v[0])) #列表元素0，转换为时间格式
            if not v[5] or isinstance(v[5], str): v[5] = 0 #列表元素5(对应数量)，如果为空，转换为0
            if not v[6] or isinstance(v[6], str): v[6] = 0 #列表元素6(对应单价)，如果为空，转换为0   
            v[7] = round(float(v[5]) * float(v[6]), 2) #列表元素7(对应金额)，金额 =  数量 *  单价       
            d = dict(zip(k,v)) 
            object_list.append(model(**d))                 
        model.objects.bulk_create(object_list, batch_size=20)
        return 'ok'
    except Exception as e:
        print(e)
        return 'err: %s. 错误工作表：%s'%(e, index+1)

def delivery_import(request):
    """批量导入 送货数据"""
    if request.method == 'GET':
        return render(request, 'web/delivery/delivery_import.html')
    
    k = ['date', 'name','num','customer','product','number',\
         'price','money','operator','note']    
    ret = post_excel_model_finance(request, 'post_file_excel', Delivery, k) 
    context = {'status': False, 'msg': '导入失败! %s' %ret} if ret[0:3] == 'err' \
        else   {'status': True, 'msg': '导入成功! 导入了%s张工作表. ' %ret}     
    return render(request, 'web/delivery/delivery_import.html',context)


def delivery_tpl(request):
    """下载送货模板"""
    #tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files', '批量导入送货模板.xlsx')
    tpl_path = 'web/files/%s' % '批量导入送货模板.xlsx'
    return down_file(tpl_path, 'delivery_excel_tpl.xlsx')
