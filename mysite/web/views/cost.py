# -*- coding: utf-8 -*-
# 销售成本模块
import os, datetime
import xlrd, json
from myAPI.excelAPI import get_date
from myAPI.downfileAPI import down_file
from myAPI.pageAPI import djangoPage, PAGE_NUM
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect, HttpResponse,\
    StreamingHttpResponse
from web.forms.cost import CostForm
from web.models import Cost
from myAPI.modelAPI import get_model_first_id, get_model_last_id, \
                        get_model_up_id, get_model_name_up_id, get_model_data, get_post_data
from myAPI.excelAPI import list_to_xlsx
from myAPI.fileAPI import downfile

def cost_id_update(request, model, id):
    """" 更新一条数据库记录。对应以下导入电子表格时的算法：
        v[7] = round(float(v[5]) - float(v[6]), 2) #毛利 =  发货额 -  成本额
        v[14] = round((v[8]+v[9]+v[10]+v[11]+v[12]+v[13]),2) #小计0
        v[21] = round((v[15]+v[16]+v[17]+v[18]+v[19]+v[20]),2) #小计1
        v[22] = round((v[14]+v[21]),2)#费用合计    
    """    
    id = int(id)
    model.filter(id=id).update(operator = request.user.username)  #更新经办人为登录用户        
    
    #更新 毛利 =  发货额 -  成本额 
    pgross_profit = round(model.get(id=id).delivery - model.get(id=id).cost_amount, 2) #金额保留2位小数
    model.filter(id=id).update(pgross_profit = pgross_profit)             
    
    #更新 小计0 = 餐费meals + 差旅费travel_expenses + 礼品gift + 礼金cash_gift + 娱乐recreation + 汽车费car
    subtotal0 = round(model.get(id=id).meals + model.get(id=id).travel_expenses\
                    + model.get(id=id).gift + model.get(id=id).cash_gift\
                    + model.get(id=id).recreation + model.get(id=id).car, 2)
    model.filter(id=id).update(subtotal0 = subtotal0)
    
    #更新 小计1 = cost_rate + return_freight + special_car + customer_claims + payment_commission + other
    subtotal1 = round(model.get(id=id).cost_rate + model.get(id=id).return_freight\
                + model.get(id=id).special_car + model.get(id=id).customer_claims\
                + model.get(id=id).payment_commission + model.get(id=id).other, 2)
    model.filter(id=id).update(subtotal1 = subtotal1)
    
    #更新费用合计 = subtotal0 + subtotal1
    total_expenses = round(subtotal0 + subtotal1, 2)
    model.filter(id=id).update(total_expenses = total_expenses)
    return ''


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
    """
    sheet = workbook.sheet_by_index(index)  
    try:
        #1.1、电子表格转换为列表；2、空行结束循环
        mylist = []
        for row_num in range(x, sheet.nrows): #从x行开始  x=0,1,2...
            row = sheet.row(row_num) #row -- [empty:'', empty:'', text:'HZ', number:10.0]           
            v = []
            for r in row: #一次处理电子表格一行                           
                v.append(r.value)
            if not any(v): #空行结束循环
                break                 
            mylist.append(v)
       
        #2.1、列表中清除空格行 和 以‘日期’开头的行；2、插入客户名称、经办人
        mlist = []
        name = ''
        filename_no = '' #未被导入的工作表名 
        for v in mylist:   
            if len(mylist) > 2:
                if v[0] != '日期': #列表中清除空格行 和 以‘日期’开头的行
                    v1 = v[:] #v1 ['送货单位名称','','','','','','','','']
                    v1.pop(0) #v1 ['','','','','','','','']
                    if isinstance(v[0], str) and not any(v1):
                        name = v[0] #获得送货单位名称；字符串开始行的第一个单元格值。
                    else:
                        v.insert(1,name) #插入 客户名称
                        v[23] = '陈会计'  #增加 经办人
                        mlist.append(v)
            else:
                v1 = v[:] 
                v1.pop(0)
                if isinstance(v[0], str) and not any(v1):
                    filename_no = v[0]
                                       
        #3.1、列表数据，初始化成与数据库字段一样的数据类型；2、数据写入数据库 
        object_list = []      
        for v in mlist:
            if isinstance(v[0], int) or isinstance(v[0], float):
                v[0] =  get_date(int(v[0])) #列表元素0，转换为时间格式
            else:
                v[0] = '1900-01-01'
            for r in  range(4,23):
                if not v[r] or isinstance(v[r], str): 
                    v[r] = 0 #数值单元格 列表元素，如果为空或为字符型，转换为0
                else:
                    v[r] = round(v[r], 2)
            v[7] = round(float(v[5]) - float(v[6]), 2) #毛利 =  发货额 -  成本额
            v[14] = round((v[8]+v[9]+v[10]+v[11]+v[12]+v[13]),2) #小计0
            v[21] = round((v[15]+v[16]+v[17]+v[18]+v[19]+v[20]),2) #小计1
            v[22] = round((v[14]+v[21]),2)#费用合计
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

def cost_import(request):
    """批量导入 销售成本数据"""
    if request.method == 'GET':
        return render(request, 'web/cost/cost_import.html')
    
    k = ["date","name","voucherno","abstract","invoice","delivery",\
         "cost_amount","pgross_profit","meals","travel_expenses","gift",\
         "cash_gift","recreation","car","subtotal0","cost_rate",\
         "return_freight","special_car","customer_claims","payment_commission","other",\
         "subtotal1","total_expenses","operator"]    
    ret = post_excel_model_finance(request, 'post_file_excel', Cost, k) 
    context = {'status': False, 'msg': '导入失败! %s' %ret} if ret[0:3] == 'err' \
        else   {'status': True, 'msg': '导入成功! %s. ' %ret}     
    return render(request, 'web/cost/cost_import.html',context)


def cost_tpl(request):
    """下载销售成本模板"""
    #tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files', '批量导入送货模板.xlsx')
    tpl_path = 'web/files/%s' % '批量导入送货模板.xlsx'
    return down_file(tpl_path, 'delivery_excel_tpl.xlsx')

def cost_list(request, page):
    """销售成本列表"""
    cleanData = request.GET.dict()
    model = Cost.objects
    if request.method == 'POST':
        page = 1
        cleanData = request.POST.dict()        
        dict.pop(cleanData,'csrfmiddlewaretoken') #删除字典中的键'csrfmiddlewaretoken'和值
   
    name, name_list, queryString, datas = get_model_data(model, cleanData)
          
    total_expenses = round(sum(datas.filter().values_list('total_expenses', flat=True)), 2) #费用合计求和    
    pgross_profit =  round(sum(datas.filter().values_list('pgross_profit', flat=True)),2)  #毛利求和
    Total_profit =  round(pgross_profit - total_expenses, 2) #利润总额 = 毛利求和 - 费用合计求和
    
    data_list, pageList, num_pages, page = djangoPage(datas,page,PAGE_NUM)  #调用分页函数
    offset = PAGE_NUM * (page - 1) 
    
    return render(request, 'web/cost/cost_list.html', context=locals())


def cost_add(request):
    """添加"""
    if request.method == 'GET':
        form = CostForm()
        return render(request, 'web/cost/cost_add.html', context=locals())
    form = CostForm(data=request.POST)
    if form.is_valid():
        form.save()
        # 更新一条数据库记录
        model = Cost.objects
        cost_id_update(request, model, get_model_last_id(model))
        return redirect('/web/cost/list/(.+)')
    return render(request, 'web/cost/cost_add.html', context=locals())


def cost_edit(request, cid):
    """编辑"""
    obj = Cost.objects.get(id=cid)
    if request.method == 'GET':
        form = CostForm(instance=obj)
        return render(request, 'web/cost/cost_edit.html', context=locals())
    form = CostForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        # 更新一条数据库记录
        model = Cost.objects
        cost_id_update(request, model, cid)
        return redirect('/web/cost/list/(.+)')
    return render(request, 'web/cost/cost_edit.html', context=locals())
 
def cost_del(request, cid):
    """删除"""
    Cost.objects.filter(id=cid).delete()
    return redirect('/web/cost/list/(.+)')

#销售成本利润图形
def profit_graph(request):
    '''利润柱状可视化图形'''                    
    profit_list = [] #利润总额
    pgross_profit_list = [] #毛利
    total_expenses_list = [] #费用
    name_list = list(set(Cost.objects.values_list('name', flat=True)))
    for name in name_list:
        total_expenses = sum(Cost.objects.filter(name=name).values_list('total_expenses', flat=True)) #费用合计求和    
        total_expenses_list.append(round(total_expenses,2))
        pgross_profit =  sum(Cost.objects.filter(name=name).values_list('pgross_profit', flat=True))  #毛利求和
        pgross_profit_list.append(round(pgross_profit,2))
        profit_list.append(round(pgross_profit - total_expenses, 2)) #利润总额 = 毛利求和 - 费用合计求和
       
    mylist = []
    k = ['name','pgross_profit_list','total_expenses_list', 'profit_list']#客户名称,毛利, 费用,利润总额
    lists =  list(zip(name_list,pgross_profit_list,total_expenses_list,profit_list)) #多个列表组成一个列表，其中元素为元组
    for (index,v) in enumerate(lists):
        d = dict(zip(k,v))
        mylist.append(d)
               
    pgross_profit = round(sum(pgross_profit_list),2) #总毛利
    total_expenses = round(sum(total_expenses_list),2) #总费用    
    total_profit = round(sum(profit_list),2) #总利润
    dataX = json.dumps(list(range(0, len(profit_list))))
    data = json.dumps(list(profit_list))    
    name = '客户利润总额'
    x_y_meg = '图例： X横轴-客户名称序号； Y纵轴-客户销售成本利润'      
    title = '客户数量(%s个) - 总毛利(%s元) - 总费用(%s元) - 总利润(%s元)' \
            %(len(name_list), pgross_profit,total_expenses, total_profit)  
    return render(request, 'web/cost/profit_graph.html', context=locals())


def convertxlsx(data_list, filePath, ids):
    ret = True
    try:
        # 数据库字段值，转化为电子表格值。 电子表格标题栏。1、与数据库字段保持一致。
        headings = ['序号','日期','客户名称','凭证号','摘要','开票额','发货额',\
                    '成本金额','毛利','餐费','差旅费','礼品','礼金','娱乐',\
                    '汽车费','小计0','费用率','退货运费','专车费用','客诉赔款','实际支付佣金','其他']
        
        date = [str(i.date + datetime.timedelta(hours=8)).split('+')[0] for i in data_list] #日期+时差                      
        name = [i.name for i in data_list]                                  
        voucherno = [i.voucherno for i in data_list]        
        abstract = [i.abstract for i in data_list ]         
        invoice = [i.invoice for i in data_list ]         
        delivery = [i.delivery for i in data_list ]         
        cost_amount = [i.cost_amount for i in data_list ]        
        pgross_profit = [i.pgross_profit for i in data_list ] 
        meals = [i.meals for i in data_list ]        
        travel_expenses = [i.travel_expenses for i in data_list ] 
        gift = [i.gift for i in data_list ]
        cash_gift = [i.cash_gift for i in data_list ]        
        recreation = [i.recreation for i in data_list ] 
        car = [i.car for i in data_list ]        
        subtotal0 = [i.subtotal0 for i in data_list ] 
        cost_rate = [i.cost_rate for i in data_list ]
        return_freight = [i.return_freight for i in data_list ]        
        special_car = [i.special_car for i in data_list ] 
        customer_claims = [i.customer_claims for i in data_list ]        
        payment_commission = [i.payment_commission for i in data_list ] 
        other = [i.other for i in data_list ]
        subtotal1 = [i.subtotal1 for i in data_list ]        
        total_expenses = [i.total_expenses for i in data_list ] 
        operator = [i.operator for i in data_list ]        
        
        data = [ids, date,name,voucherno,abstract,invoice,delivery,\
        cost_amount,pgross_profit,meals,travel_expenses,gift,\
        cash_gift,recreation,car,subtotal0,cost_rate,\
        return_freight,special_car,customer_claims,payment_commission,other,\
        subtotal1,total_expenses,operator ]
        if not list_to_xlsx(data, headings, filePath): # 保存为电子表格
            ret = False
    except Exception as _e:
        print('err: %s' %_e)
        ret = False
    return ret

#单页保存Excel
def cost_makexlsx_page(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Cost.objects)
    datas, pageList, num_pages, page = djangoPage(datas, page, PAGE_NUM)  #调用分页函数
    ids = [i+PAGE_NUM * (page - 1) for i in range(1,PAGE_NUM+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return downfile(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/delivery/list/%s' % (page))

#全部保存Excel
def cost_makexlsx_all(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Cost.objects)
    ids = [i for i in range(1,len(datas)+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return downfile(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/delivery/list/%s' % (page))

