# -*- coding: utf-8 -*-
# 领料汇总 模块
import os,datetime, xlrd, json
from web.models import Picking
from myAPI.excelAPI import get_date, list_to_xlsx
from django.shortcuts import render, redirect
from myAPI.pageAPI import djangoPage, PAGE_NUM
from myAPI.downfileAPI import down_file
from web.forms.picking import PickingForm
from myAPI.modelAPI import get_model_first_id, get_model_last_id, \
    get_model_up_id, get_model_name_up_id, get_model_data, get_post_data
from myAPI.listAPI import pinyin
from django.http.response import HttpResponseRedirect, StreamingHttpResponse
from myAPI.listAPI import pinyin 

def model_id_update(request, model, id):
    """" 更新一条数据库记录。
        v[6] = round(float(v[5]) * float(v[4]), 2) #金额 =  数量 *  单价
    """    
    id = int(id)    
    model.filter(id=id).update(operator = request.user.username)  #更新经办人为登录用户
    
    #更新 金额 =  数量 *  单价 
    money = round(model.get(id=id).number * model.get(id=id).univalence, 2) #金额保留2位小数
    model.filter(id=id).update(money = money)             
       
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
        for row_num in range(x, sheet.nrows): #从x行开始  x=0,1,2...    row_num=0,1,2,3,...
            row = sheet.row(row_num) #row -- [empty:'', empty:'', text:'HZ', number:10.0]           
            v = []
            for r in row: #一次处理电子表格一行                           
                v.append(r.value)                              
            if not any(v) and row_num >= 2: #空行 v=['','','','','','',''] 结束循环
                break                                
            mylist.append(v)
            
        
        
        #2.1、列表中去掉列表最后两个元素；2、插入客户名称、经办人
        mlist = []
        name = ''
        filename_no = '' #未被导入的工作表名 
        for (n,v) in enumerate(mylist):    
            v1 = v[1:] #v ['名称','','','','','','','']  v1['','','','','','','']
            if n == 0 and not any(v1):
                name = v[0] #获得名称
            else:
                v.insert(1, name) #插入 名称
                v.insert(9, '陈会计')  #插入 经办人
            if n >= 2:    
                mlist.append(v)
                                         
        #3.1、列表数据，初始化成与数据库字段一样的数据类型；2、数据写入数据库 
        object_list = []      
        for (n,v) in enumerate(mlist):                                  
            if isinstance(v[0], int) or isinstance(v[0], float):
                v[0] =  get_date(int(v[0])) #列表元素0，转换为时间格式
            else:
                v[0] = '1900-01-01'
                            
            for r in range(4,7):
                if not v[r] or isinstance(v[r], str): 
                    v[r] = 0 #数值单元格 列表元素，如果为空或为字符型，转换为0
                else:
                    v[r] = round(v[r], 2)
                                                                          
            v[6] = round(float(v[5]) * float(v[4]), 2) #金额 =  数量 *  单价
            
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
  
def picking_import(request):
    """批量导入材料报表"""
    down_tpl = '/web/picking/tpl/'  #下载模板路径
    
    if request.method == 'GET':
        return render(request, 'web/import.html',context=locals())
    
    k = ["date", "name","receipt","material_name","number",\
         "univalence","money","product_name","remarks","operator"]  
       
    ret = post_excel_model(request, 'post_file_excel', Picking, k) 
    context = {'status': False, 'msg': '导入失败! %s' %ret} if ret[0:3] == 'err' \
        else  {'status': True, 'msg': '导入成功! %s. ' %ret}     
    return render(request, 'web/import.html',context)
  
def picking_tpl(request):
    """下载材料报表模板"""
    tpl_path = 'web/files/%s' % '批量导入领料汇总模板.xlsx' 
    return down_file(tpl_path, 'excel_tpl.xlsx')
  
def picking_list(request, page):
    """材料报表列表"""
    cleanData = request.GET.dict()
    model = Picking.objects
    if request.method == 'POST':
        cleanData = request.POST.dict()          
        dict.pop(cleanData,'csrfmiddlewaretoken') 
                           
    page = int(cleanData.get('page',1))
    name, name_list, queryString, datas = get_model_data(model, cleanData)
                
    moneys = round(sum(datas.filter().values_list('money', flat=True)), 2)  #金额 求和    

    data_list, pageList, num_pages, page = djangoPage(datas,page,PAGE_NUM)  #调用分页函数
    offset = PAGE_NUM * (page - 1) 
    name_list = pinyin(list(set(model.values_list('name', flat=True))))    
    name_list.insert(0, '')
    return render(request, 'web/picking/picking_list.html', context=locals())


def picking_add(request):
    """添加"""
    if request.method == 'GET':
        form = PickingForm()
        return render(request, 'web/form_submit.html', context=locals())
    form = PickingForm(data=request.POST)
    if form.is_valid():
        form.save()
        # 更新一条数据库记录
        model = Picking.objects
        model_id_update(request, model, get_model_last_id(model))
        return redirect('/web/picking/list/(.+)')
    return render(request, 'web/form_submit.html', context=locals())
  
  
def picking_edit(request, cid):
    """编辑"""
    obj = Picking.objects.get(id=cid)
    if request.method == 'GET':
        form = PickingForm(instance=obj)
        return render(request, 'web/form_submit.html', context=locals())
    form = PickingForm(data=request.POST, instance=obj)    
    if form.is_valid():
        form.save()
        # 更新一条数据库记录
        model = Picking.objects
        model_id_update(request, model, cid)
        return redirect('/web/picking/list/(.+)')
    return render(request, 'web/form_submit.html', context=locals())
   
def picking_del(request, cid):
    """删除"""
    Picking.objects.filter(id=cid).delete()
    return redirect('/web/picking/list/(.+)')


def convertxlsx(data_list, filePath, ids): 
    ret = True
    try:
        # 数据库字段值，转化为电子表格值。 电子表格标题栏。1、与数据库字段保持一致。
        headings = ['序号', '日期','名称','领料单号码','材料名称及规格',\
                    '数量','单价','金额','产品名称','备注','经办人']
                
        date = [str(i.date + datetime.timedelta(hours=8)).split('+')[0] for i in data_list] #日期+时差                      
        name = [i.name for i in data_list]                                  
        receipt = [i.product_name for i in data_list]        
        material_name = [i.material_name for i in data_list ] 
                   
        number = [i.number for i in data_list ]         
        univalence = [i.univalence for i in data_list ]        
        money = [i.money for i in data_list ] 
        product_name = [i.product_name for i in data_list ] 
        remarks = [i.remarks for i in data_list ]        
        operator = [i.operator for i in data_list ] 
                 
        data = [ids, date, name, receipt, material_name,\
                number, univalence, money, product_name, remarks, operator]
        
        if not list_to_xlsx(data, headings, filePath): # 保存为电子表格
            ret = False
    except Exception as _e:
        print('err: %s' %_e)
        ret = False
    return ret

#单页保存Excel  down_file
def picking_makexlsx_page(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Picking.objects)
    datas, pageList, num_pages, page = djangoPage(datas, page, PAGE_NUM)  #调用分页函数
    ids = [i+PAGE_NUM * (page - 1) for i in range(1,PAGE_NUM+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return down_file(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/picking/list/%s' % (page))

#全部保存Excel
def picking_makexlsx_all(request, page):
    datas, tempFilePath, fileName = get_post_data(request, Picking.objects)
    ids = [i for i in range(1,len(datas)+1) ]  #序号
    if convertxlsx(datas, tempFilePath, ids):
        return down_file(tempFilePath, fileName)
    return HttpResponseRedirect(r'/web/picking/list/%s' % (page))


