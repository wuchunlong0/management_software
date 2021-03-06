# -*- coding: utf-8 -*-
# 应付账款模块
import os
import datetime
import xlrd,json
from web.models import Copewith
from myAPI.excelAPI import get_date
from django.shortcuts import render, redirect
from myAPI.pageAPI import djangoPage, PAGE_NUM
from myAPI.downfileAPI import down_file
from django.http.response import HttpResponseRedirect, HttpResponse,\
    StreamingHttpResponse
from web.forms.copewith import CopewithForm
from myAPI.modelAPI import get_model_first_id, get_model_last_id, \
                            get_model_up_id, get_model_name_up_id, get_model_data, get_post_data
from myAPI.excelAPI import list_to_xlsx
from myAPI.fileAPI import downfile


def copewith_id_update(request, model, id):
    """" 更新一条数据库记录。对应以下导入电子表格时的算法：
        v8, v13 = 0, 0
        v[7] = round(float(v[5]) * float(v[6]), 2) #金额 =  收货数量 *  单价
        if n > 0: 
            #v[8] = round((mlist[n-1][8] + v[7] - v[4]), 2) #余额 = 余额_1 + 金额 - 付款
            #v[13] =  mlist[n-1][13] +  v[7] - v[12]  #欠票 = 欠票_1 + 金额 - 金额1
            v[8] = round((v8 + v[7] - v[4]), 2) #余额 = 余额_1 + 金额 - 付款
            v[13] =  v13 +  v[7] - v[12]  #欠票 = 欠票_1 + 金额 - 金额1
            v8, v13 = v[8], v[13]
    """    
    id = int(id)
    model.filter(id=id).update(operator = request.user.username)  #更新经办人为登录用户    

    #更新 金额 =  收货数量 *  单价 
    money = round(model.get(id=id).number * model.get(id=id).univalence, 2) #金额保留2位小数
    model.filter(id=id).update(money = money)             
    
    if id > 1:
        balance_1 = model.get(id=get_model_up_id(model, id)).balance
        balance = round(balance_1 + money - model.get(id=id).payment, 2) #余额 = 余额_1 + 金额 - 付款
        model.filter(id=id).update(balance = balance)             
    
        owe_ticket_1 = model.get(id=get_model_up_id(model, id)).owe_ticket
        owe_ticket = round(owe_ticket_1 + money - model.get(id=id).money1, 2) #欠票 = 欠票_1 + 金额 - 金额1
        model.filter(id=id).update(owe_ticket = owe_ticket)             

    return ''


def post_excel_model(request, post_file_excel, model, k):
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
    filename_no = ''
    n, n1 = 0, 0  # n序号   n1 未被导入数据的工作表记数
    for index in range(0, sheet_sum):
        ret = workbook_cost(workbook, 0, index, model, k) #从电子表格0行开始
        if ret[0:3] == 'err':
            return ret
        else:
          n += 1
          if ret:
              n1 += 1 #n1 未被导入数据的工作表记数
              filename_no += str(n)+ '. ' + ret + '、' #n序号          
    return  "导入了%s工作张表。未被导入数据的工作表总数：%s； 表名：%s"%(str(sheet_sum), str(n1), filename_no)

def workbook_cost(workbook, x, index, model, k):
    """ 电子表格，多张工作表写入数据库
        workbook: workbook = xlrd.open_workbook(file_contents=file_excel.file.read())
        x: 从x行开始  x=0,1,2...
        index: 工作表序号
        model: 数据库
        K: 数据库字段, 与Excel表格列对应
        结束循环条件:  最后两行相同       
    """
    sheet = workbook.sheet_by_index(index)  
    try:
        #1.1、电子表格转换为列表；2、最后两行相同结束循环
        mylist = []
        for row_num in range(x, sheet.nrows): #从x行开始  x=0,1,2...
            row = sheet.row(row_num) #row -- [empty:'', empty:'', text:'HZ', number:10.0]           
            v = []
            for r in row: #一次处理电子表格一行                           
                v.append(r.value) 
            v.pop(9) #去掉列表的空列                
            mylist.append(v)
            if (len(mylist) > 3) and (mylist[-1] == mylist[-2]): #最后两行相同结束循环
                break                                
        
        #2.1、列表中去掉列表最后两个元素；2、插入客户名称、经办人
        mlist = []
        name = ''
        filename_no = '' #未被导入的工作表名 
        for (n,v) in enumerate(mylist): 
        #for (n,v) in enumerate(mylist[:-2]): #去掉列表最后两个元素？？？     
            v1 = v[2:] #v ['**','单位名称','','','','','','','']  v1['','','','','','','']
            if n == 0 and not any(v1):
                name = v[1] #获得单位名称
            else:
                v.insert(1, name) #插入 客户名称
                v.insert(14, '陈会计')  #插入 经办人
            if n >= 4:    
                mlist.append(v)
                                        
        #3.1、列表数据，初始化成与数据库字段一样的数据类型；2、数据写入数据库 
        object_list = []      
        v8, v13 = 0, 0
        for (n,v) in enumerate(mlist):
            if isinstance(v[0], int) or isinstance(v[0], float):
                v[0] =  get_date(int(v[0])) #列表元素0，转换为时间格式
            else:
                v[0] = '1900-01-01'

            if isinstance(v[10], int) or isinstance(v[10], float):
                v[10] =  get_date(int(v[10])) #列表元素0，转换为时间格式
            else:
                v[10] = '1900-01-01'
                
            for r in  range(4,9):
                if not v[r] or isinstance(v[r], str): 
                    v[r] = 0 #数值单元格 列表元素，如果为空或为字符型，转换为0
                else:
                    v[r] = round(v[r], 2)
            for r in  range(12,14):
                if not v[r] or isinstance(v[r], str): 
                    v[r] = 0 #数值单元格 列表元素，如果为空或为字符型，转换为0
                else:
                    v[r] = round(v[r], 2)
                                                           
            v[7] = round(float(v[5]) * float(v[6]), 2) #金额 =  收货数量 *  单价
            if n > 0: 
                v[8] = round((v8 + v[7] - v[4]), 2) #余额 = 余额_1 + 金额 - 付款
                v[13] =  v13 +  v[7] - v[12]  #欠票 = 欠票_1 + 金额 - 金额1
                v8, v13 = v[8], v[13]
            d = dict(zip(k,v)) 
            object_list.append(model(**d)) 
                             
        if object_list:
            model.objects.bulk_create(object_list, batch_size=20)
        else:
            filename_no += '%s' %(index+1)
            
        return filename_no
    except Exception as e:
        print(e)
        return 'err: %s. 错误工作表：%s'%(e, index+1)

def copewith_import(request):
    """批量导入应付账款"""
    if request.method == 'GET':
        return render(request, 'web/copewith/copewith_import.html')
    
    k = ["date","name","receipt","abstract","payment","number","univalence",\
         "money","balance","note","date1","Invoice_number",\
         "money1","owe_ticket","operator"]    
    ret = post_excel_model(request, 'post_file_excel', Copewith, k) 
    context = {'status': False, 'msg': '导入失败! %s' %ret} if ret[0:3] == 'err' \
        else  {'status': True, 'msg': '导入成功! %s. ' %ret}     
    return render(request, 'web/copewith/copewith_import.html',context)

def copewith_tpl(request):
    """下载应付账款模板"""
    tpl_path = 'web/files/%s' % '批量导入应付账款模板.xlsx'
    return down_file(tpl_path, 'copewith_excel_tpl.xlsx')


def copewith_list(request, page):
    """应付账款列表"""
    cleanData = request.GET.dict()
    model = Copewith.objects
    if request.method == 'POST':
        page = 1
        cleanData = request.POST.dict()
        dict.pop(cleanData,'csrfmiddlewaretoken') 
   
    name, name_list, queryString, datas = get_model_data(model, cleanData)
          
    payments = round(sum(datas.filter().values_list('payment', flat=True)), 2)  #付款 求和
    moneys = round(sum(datas.filter().values_list('money', flat=True)), 2)  #金额 求和    
    money1s = round(sum(datas.filter().values_list('money1', flat=True)),2)   #金额1 求和
    owe_tickets = round(sum(datas.filter().values_list('owe_ticket', flat=True)),2) #欠票 求和
    if get_model_first_id(datas):
        balances = datas.get(id=get_model_first_id(datas)).balance # 倒数最后一条记录      
    data_list, pageList, num_pages, page = djangoPage(datas,page,PAGE_NUM)  #调用分页函数
    offset = PAGE_NUM * (page - 1)  
    return render(request, 'web/copewith/copewith_list.html', context=locals())

def copewith_add(request):
    """添加"""
    if request.method == 'GET':
        form = CopewithForm()
        return render(request, 'web/copewith/copewith_add.html', context=locals())
    form = CopewithForm(data=request.POST)
    if form.is_valid():
        form.save()
        # 更新一条数据库记录
        model = Copewith.objects
        copewith_id_update(request, model, get_model_last_id(model))
        return redirect('/web/copewith/list/(.+)')
    return render(request, 'web/copewith/copewith_add.html', context=locals())


def copewith_edit(request, cid):
    """编辑"""
    obj = Copewith.objects.get(id=cid)
    if request.method == 'GET':
        form = CopewithForm(instance=obj)
        return render(request, 'web/copewith/copewith_edit.html', context=locals())
    form = CopewithForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        # 更新一条数据库记录
        model = Copewith.objects
        copewith_id_update(request, model, cid)
        return redirect('/web/copewith/list/(.+)')
    return render(request, 'web/copewith/copewith_edit.html', context=locals())
 
def copewith_del(request, cid):
    """删除"""
    Copewith.objects.filter(id=cid).delete()
    return redirect('/web/copewith/list/(.+)')

def convertxlsx(data_list, filePath, ids):
    ret = True
    try:
        # 数据库字段值，转化为电子表格值。 电子表格标题栏。1、与数据库字段保持一致。
        headings = ['序号','日期','客户名称','收货单号码','摘要','付款','收货数量',\
                    '单价','金额','余额','备注','日期1','发票号码','金额1',\
                    '欠票','经办人']
        
        date = [str(i.date + datetime.timedelta(hours=8)).split('+')[0] for i in data_list] #日期+时差                      
        name = [i.name for i in data_list]                                  
        receipt = [i.receipt for i in data_list]        
        abstract = [i.abstract for i in data_list ]         
        payment = [i.payment for i in data_list ]         
        number = [i.number for i in data_list ]         
        univalence = [i.univalence for i in data_list ]        
        money = [i.money for i in data_list ] 
        balance = [i.balance for i in data_list ]        
        note = [i.note for i in data_list ] 
        date1 = [str(i.date1 + datetime.timedelta(hours=8)).split('+')[0] for i in data_list] #日期+时差                      
        Invoice_number = [i.Invoice_number for i in data_list ]        
        money1 = [i.money1 for i in data_list ] 
        owe_ticket = [i.owe_ticket for i in data_list ]        
        operator = [i.operator for i in data_list ]                
        
        data = [ids, date,name,receipt,abstract,payment,number,univalence,\
        money,balance,note,date1,Invoice_number,money1,owe_ticket,operator ]
        if not list_to_xlsx(data, headings, filePath): # 保存为电子表格
            ret = False
    except Exception as _e:
        print('err: %s' %_e)
        ret = False
    return ret

#单页保存Excel
def copewith_makexlsx_page(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Copewith.objects)
    datas, pageList, num_pages, page = djangoPage(datas, page, PAGE_NUM)  #调用分页函数
    ids = [i+PAGE_NUM * (page - 1) for i in range(1,PAGE_NUM+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return downfile(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/copewith/list/%s' % (page))

#全部保存Excel
def copewith_makexlsx_all(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Copewith.objects)
    ids = [i for i in range(1,len(datas)+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return downfile(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/copewith/list/%s' % (page))


