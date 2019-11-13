# -*- coding: utf-8 -*-
# 材料报表 模块
import os,datetime, xlrd, json
from web.models import Materialreport
from myAPI.excelAPI import get_date, list_to_xlsx
from django.shortcuts import render, redirect
from myAPI.pageAPI import djangoPage, PAGE_NUM
from myAPI.downfileAPI import down_file
from web.forms.materialreport import MaterialreportForm
from myAPI.modelAPI import get_model_first_id, get_model_last_id, \
    get_model_up_id, get_model_name_up_id, get_model_data, get_post_data
from myAPI.listAPI import pinyin
from django.http.response import StreamingHttpResponse
from myAPI.listAPI import pinyin 
def model_id_update(request, model, id):
    """" 更新一条数据库记录。
        v[5] = round(float(v[4]) * float(v[3]), 2) #上月结存金额 =  数量 *  单价
        v[8] = round(float(v[7]) * float(v[6]), 2) #收入金额 =  数量 *  单价
        v[11] = round(float(v[10]) * float(v[9]), 2) #加权金额 =  数量 *  单价
        v[14] = round(float(v[13]) * float(v[12]), 2) #生产支出金额 =  数量 *  单价
        v[21] = round(float(v[20]) * float(v[19]), 2) #本月结存金额 =  数量 *  单价

    """    
    id = int(id)    
    model.filter(id=id).update(operator = request.user.username)  #更新经办人为登录用户
    
    #更新 上月结存金额 =  数量 *  单价 
    lastmonth_money = round(model.get(id=id).lastmonth_number * model.get(id=id).lastmonth_univalence, 2) #金额保留2位小数
    model.filter(id=id).update(lastmonth_money = lastmonth_money)             
       
    #更新 收入金额 =  数量 *  单价
    income_money = round(model.get(id=id).income_number * model.get(id=id).income_univalence, 2) #金额保留2位小数
    model.filter(id=id).update(income_money = income_money) 
    
    #更新 加权金额 =  数量 *  单价 
    weighting_money = round(model.get(id=id).weighting_number * model.get(id=id).weighting_univalence, 2) #金额保留2位小数
    model.filter(id=id).update(weighting_money = weighting_money)                 

    #更新 生产支出金额 =  数量 *  单价    
    production_expenditure_money = round(model.get(id=id).production_expenditure_number * model.get(id=id).production_expenditure_univalence, 2) #金额保留2位小数
    model.filter(id=id).update(production_expenditure_money = production_expenditure_money)                 

    #更新 本月结存金额 =  数量 *  单价
    thismonth_money = round(model.get(id=id).thismonth_number * model.get(id=id).thismonth_univalence, 2) #金额保留2位小数
    model.filter(id=id).update(thismonth_money = thismonth_money) 
    
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
        ret = workbook_model(workbook, 0, index, model, k) #从电子表格0行开始
        if ret[0:3] == 'err':
            return ret
        else:
          n += 1
          if ret:
              n1 += 1 #n1 未被导入数据的工作表记数
              filename_no += str(n)+ '. ' + ret + '、' #n序号          
    return  "导入了%s工作张表。未被导入数据的工作表总数：%s； 表名：%s"%(str(sheet_sum), str(n1), filename_no)
  
def workbook_model(workbook, x, index, model, k):
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
            mylist.append(v)
            if not any(v): #空行 v=['','','','','','',''] 结束循环
                break                                          
        
        #2.1、列表中去掉列表最后两个元素；2、插入客户名称、经办人
        mlist = []
        name = ''
        filename_no = '' #未被导入的工作表名 
        for (n,v) in enumerate(mylist):    
            v1 = v[1:] #v ['产品名称','','','','','','','']  v1['','','','','','','']
            if n == 0 and not any(v1):
                name = v[0] #获得单位名称
            else:
                v.insert(1, name) #插入 客户名称
                v.insert(22, '陈会计')  #插入 经办人
            if n >= 3:    
                mlist.append(v)
                                           
        #3.1、列表数据，初始化成与数据库字段一样的数据类型；2、数据写入数据库 
        object_list = []      
        for (n,v) in enumerate(mlist):
            if isinstance(v[0], int) or isinstance(v[0], float):
                v[0] =  get_date(int(v[0])) #列表元素0，转换为时间格式
            else:
                v[0] = '1900-01-01'
                      
            for r in  range(3,22):
                if not v[r] or isinstance(v[r], str): 
                    v[r] = 0 #数值单元格 列表元素，如果为空或为字符型，转换为0
                else:
                    v[r] = round(v[r], 2)
                                                                          
#             v[5] = round(float(v[4]) * float(v[3]), 2) #上月结存金额 =  数量 *  单价
#             v[8] = round(float(v[7]) * float(v[6]), 2) #收入金额 =  数量 *  单价
#             v[11] = round(float(v[10]) * float(v[9]), 2) #加权金额 =  数量 *  单价
#             v[14] = round(float(v[13]) * float(v[12]), 2) #生产支出金额 =  数量 *  单价
#            v[21] = round(float(v[20]) * float(v[19]), 2) #本月结存金额 =  数量 *  单价
            
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
  
def materialreport_import(request):
    """批量导入材料报表"""
    down_tpl = '/web/materialreport/tpl/'  #下载模板路径
    
    if request.method == 'GET':
        return render(request, 'web/import.html',context=locals())
      
    k = ["date","name","material_name",\
        "lastmonth_number","lastmonth_univalence","lastmonth_money",\
        "income_number","income_univalence","income_money",\
        "weighting_number","weighting_univalence","weighting_money",\
        "production_expenditure_number","production_expenditure_univalence","production_expenditure_money",\
        "material_expenditure_number","material_expenditure_money",\
        "sale_number","sale_money",\
        "thismonth_number","thismonth_univalence","thismonth_money","operator"]    
    ret = post_excel_model(request, 'post_file_excel', Materialreport, k) 
    context = {'status': False, 'msg': '导入失败! %s' %ret} if ret[0:3] == 'err' \
        else  {'status': True, 'msg': '导入成功! %s. ' %ret}     
    return render(request, 'web/import.html',context)
  
def materialreport_tpl(request):
    """下载材料报表模板"""
    tpl_path = 'web/files/%s' % '批量导入材料报表模板.xlsx' 
    return down_file(tpl_path, 'excel_tpl.xlsx')
  
def materialreport_list(request, page):
    """材料报表列表"""
    cleanData = request.GET.dict()
    model = Materialreport.objects
    if request.method == 'POST':
        page = 1
        cleanData = request.POST.dict()          
        dict.pop(cleanData,'csrfmiddlewaretoken')                    

    name, name_list, queryString, datas = get_model_data(model, cleanData)            
    lastmonth_money = round(sum(datas.filter().values_list('lastmonth_money', flat=True)), 2)  #上月结存金额 求和    
    income_money = round(sum(datas.filter().values_list('income_money', flat=True)),2)   #收入金额 求和
    weighting_money = round(sum(datas.filter().values_list('weighting_money', flat=True)),2) #加权金额 求和    
    production_expenditure_money = round(sum(datas.filter().values_list('production_expenditure_money', flat=True)),2) #生产支出金额 求和
    material_expenditure_money = round(sum(datas.filter().values_list('material_expenditure_money', flat=True)),2) #材料支出金额 求和
    sale_money = round(sum(datas.filter().values_list('sale_money', flat=True)),2) #销售金额 求和
    thismonth_money = round(sum(datas.filter().values_list('thismonth_money', flat=True)),2) #本月结存金额 求和

    data_list, pageList, num_pages, page = djangoPage(datas,page,PAGE_NUM)  #调用分页函数
    offset = PAGE_NUM * (page - 1) 
    name_list = pinyin(list(set(Materialreport.objects.values_list('name', flat=True))))    
    name_list.insert(0, '')
    return render(request, 'web/materialreport/materialreport_list.html', context=locals())


def materialreport_add(request):
    """添加"""
    if request.method == 'GET':
        form = MaterialreportForm()
        return render(request, 'web/form_submit.html', context=locals())
    form = MaterialreportForm(data=request.POST)
    if form.is_valid():
        form.save()
        # 更新一条数据库记录
        model = materialreport.objects
        model_id_update(request, model, get_model_last_id(model))
        return redirect('/web/materialreport/list/(.+)')
    return render(request, 'web/form_submit.html', context=locals())
  
  
def materialreport_edit(request, cid):
    """编辑"""
    obj = Materialreport.objects.get(id=cid)
    if request.method == 'GET':
        form = MaterialreportForm(instance=obj)
        return render(request, 'web/form_submit.html', context=locals())
    form = MaterialreportForm(data=request.POST, instance=obj)    
    if form.is_valid():
        form.save()
        # 更新一条数据库记录
        model = Materialreport.objects
        model_id_update(request, model, cid)
        return redirect('/web/materialreport/list/(.+)')
    return render(request, 'web/form_submit.html', context=locals())
   
def materialreport_del(request, cid):
    """删除"""
    Materialreport.objects.filter(id=cid).delete()
    return redirect('/web/receivable/list/(.+)')

def convertxlsx(data_list, filePath, ids): #??
    ret = True
    try:
        # 数据库字段值，转化为电子表格值。 电子表格标题栏。1、与数据库字段保持一致。
        headings = ["序号", "采购日期", "客户名称", "送货单号码","摘要", \
                    "送货数量", "单价", "金额", "收款", "余额", "备注", \
                    "日期1", "发票号码", "金额1", "欠客户票","经办人"]
        
        k = ["date","name","receipt","abstract","number",\
            "univalence","money","collection","balance","note",\
            "date1","Invoice_number","money1","owe_ticket","operator"]  
        
        date = [str(i.date + datetime.timedelta(hours=8)).split('+')[0] for i in data_list] #日期+时差                      
        name = [i.name for i in data_list]                                  
        receipt = [i.receipt for i in data_list]        
        abstract = [i.abstract for i in data_list ]            
        number = [i.number for i in data_list ]         
        univalence = [i.univalence for i in data_list ]        
        money = [i.money for i in data_list ] 
        collection = [i.collection for i in data_list ] 
        balance = [i.balance for i in data_list ]        
        note = [i.note for i in data_list ] 
        date1 = [str(i.date1 + datetime.timedelta(hours=8)).split('+')[0] for i in data_list] #日期+时差                      
        Invoice_number = [i.Invoice_number for i in data_list ]        
        money1 = [i.money1 for i in data_list ] 
        owe_ticket = [i.owe_ticket for i in data_list ]        
        operator = [i.operator for i in data_list ]                
        
        data = [ids, date,name,receipt,abstract,number,univalence,\
        money,collection,balance,note,date1,Invoice_number,money1,owe_ticket,operator ]
        if not list_to_xlsx(data, headings, filePath): # 保存为电子表格
            ret = False
    except Exception as _e:
        print('err: %s' %_e)
        ret = False
    return ret

#单页保存Excel  down_file
def materialreport_makexlsx_page(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Materialreport.objects)
    datas, pageList, num_pages, page = djangoPage(datas, page, PAGE_NUM)  #调用分页函数
    ids = [i+PAGE_NUM * (page - 1) for i in range(1,PAGE_NUM+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return down_file(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/materialreport/list/%s' % (page))

#全部保存Excel
def materialreport_makexlsx_all(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Materialreport.objects)
    ids = [i for i in range(1,len(datas)+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return down_file(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/materialreport/list/%s' % (page))


