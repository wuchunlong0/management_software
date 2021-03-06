# -*- coding: utf-8 -*-
import os
import xlrd
import xlsxwriter
import time
import datetime
from decimal import * #浮点数保留2位小数
from django.shortcuts import render, redirect, HttpResponse
from xlrd import xldate_as_tuple

def get_date(date_int):
  """ 43250 --> 2018-05-30;  61 --> 1900-03-01"""
  date = xldate_as_tuple(date_int,0)
  value = datetime.datetime(*date)
  return str(value).split(' ')[0]

def get_model_first_id(model):
    """ 获得数据库第一条记录的id"""
    name = model.objects.filter().first()
    return model.objects.filter(name = name).first().id




# def get_workbook(request, post_file_excel):
#     post_excel = request.FILES.get(post_file_excel)
#     ext = os.path.splitext(post_excel.name)[1]    
#     if 'xls' not in ext and 'xlsx' not in ext:
#         return 'err: 请上传Excel文件'        
#     return post_excel
#     #xlrd.open_workbook(file_contents=post_excel.file.read())    
# 
# def post_excel_model_names(request, post_file_excel, model, k):
#     '''上传的Excel文件，导入数据库(Bankemploye)'''
#     post_excel = get_workbook(request, post_file_excel)
#     if post_excel[0:3] == 'err':
#         return post_excel
#     workbook = xlrd.open_workbook(file_contents=post_excel.file.read())
#     return excel_sheet_name(post_file_excel, workbook, model, k)

def post_excel_model_names(request, post_file_excel, model, k):
    '''上传的Excel文件，导入数据库(Bankemploye)'''
    user_excel = request.FILES.get(post_file_excel)
    ext = os.path.splitext(user_excel.name)[1]    
    if 'xls' not in ext and 'xlsx' not in ext:
        print('err: 请上传Excel文件')
        return False
          
    workbook = xlrd.open_workbook(file_contents=user_excel.file.read())
    return excel_sheet_name(user_excel, workbook, model, k)

def excel_sheet_name(file_excel, workbook, model, k):
    """Excel文件(单元格合并的电子表格同样适用)，导入数据库 name-防重复写入
    打开上传的Excel文件
    user_excel = request.FILES.get(post_file_excel)
    workbook = xlrd.open_workbook(file_contents=user_excel.file.read())  
    
    打开本地Excel文件
    workbook = xlrd.open_workbook(filename='本地文件路径.xlsx')  
    
    model：  数据库（Bankemploye）
    数据库(Bankemploye)字段 与Excel表格列 对应
    k = ['serialNumber', 'title', 'subitem', 'drivingfactors', 'investigation',\
         'classificationNumber', 'score', 'dimensionalItems', 'remarks']    
    """
    sheet = workbook.sheet_by_index(0)      
    try:
        mylist = []
        object_list = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row(row_num)            
            v = []
            for (index,r) in enumerate(row):                
                s = r.value
                if s:
                    v.append(s.strip()) if isinstance(s, str) else v.append(int(s)) 
                else:
                    if row_num == 1:
                        v.append(s.strip()) if isinstance(s, str) else v.append(int(s)) 
                    else: 
                        v.append(mylist[row_num-2][index])                                
            mylist.append(v)
            
        #添加记录 
        n = 0
        for i in mylist:
            if model.objects.filter(name=i[0]):
                pass  #重复记录 pass
            else:
                u = model()            
                u.name = i[0]
                u.password = i[1]
                u.email = i[2]
                u.save()
                n += 1    
                     
        print('电子表格导入成功. %s. %s条记录' %(file_excel, n))
        return True
    except Exception as e:
        print('err: %s.  ' %(e))
        return False



def get_excel_x_y(file_excel, x, y):
    '''获得电子表格[x，y]单元格值，返回字符串。单元格从[0，0]开始。'''
    workbook = xlrd.open_workbook(filename = file_excel)
    sheet = workbook.sheet_by_index(0)
    return sheet.row(x)[y].value

# def isSerialNumber(model):
#     '''判断数据库序号字段是否从0开始，步长1，连续 0、1、2、3、...'''
#     investigation_list = model.objects.values_list('serialNumber', flat=True)
#     return [str(n) for n in range(0,investigation_list.count())] == list(investigation_list)

def list_to_xlsx(data, headings, filePath):
    """import xlsxwriter
    列表保存为电子表格文件 
    data形如[[id1,id2,id3, ...], ['title1','title2','title3', ...], ['sum1','sum2','sum3', ...],...]数据 , 
    headings电子表格标题: headings = ['id','title','sum','a','b','c','d','e']
    filePath电子表格文件 文件路径 ../excel.xlsx。   
    """
    ret = True
    try:
        A = 65 # 'A'
        workbook = xlsxwriter.Workbook(filePath)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})  
        worksheet.write_row('A1', headings, bold)
        for n in range(len(headings)):
            if n < 26:
                worksheet.write_column(chr(A + n) +'2', data[n])
            else:
                worksheet.write_column('A'+chr(A + n-26) +'2', data[n])
        workbook.close() 
    except Exception as e:       
        print('list_to_xlsx err: %s' %(e))
        ret = False    
    return ret 


# # 列表保存为电子表格。data形如[['data1',...],['data1',...],...]数据 , headings电子表格标题，电子表格标题栏，与数据库字段保持一致。参见models.py Order数据库字段； filePath文件路径
# def savexlsx(data, headings, filePath):
#     A = 65 # 'A'
#     workbook = xlsxwriter.Workbook(filePath)
#     worksheet = workbook.add_worksheet()
#     bold = workbook.add_format({'bold': 1})  #如何控制单元格宽度？  
#     worksheet.write_row('A1', headings, bold)
#     for n in range(len(headings)):
#         worksheet.write_column(chr(A + n) +'2', data[n])
#     workbook.close() 
#     return ''       


def list_to_htmlTableStr(datas):
    """
    列表转换成便于网页显示的表格(边框表格)字符串
    datas: [["id", "title", "name", "sum"],
            [ 0,  "中国",  "李大庆", 100],
            [ 1,  "美国",  "张小平", 200],
            [ 2,  "德国",  "赵一曼", 300]]   
    """    
    s = "<table class='table table-bordered'>"    
    for (i,data) in enumerate(datas):
        if not i:
            s += "<thead><tr>"
            for d in data:
                s += "<th>%s</th>" %d
            s += "</tr></thead><tbody>"
        else:   
            s += "<tr>"
            for d in data:                        
                s += "<td>%s</td>" % d            
            s += "</tr>"   
    s += "</tbody></table>"
    return s

def xlsx_to_yield(filename_xls):
    """xlsx文件转换成列表 
    filename_xls 电子表格文件格式 test.xlsx 
    A       B       C       D
    1       2       3       4            
    中国    美国    德国     英国
    print(list(xlsx_to_yield('bank/files/test.xlsx')))            
    [['A', 'B', 'C', 'D'], [1.0, 2.0, 3.0, 4.0], ['中国', '美国', '德国', '英国']]   
    """    
    try:
        table = xlrd.open_workbook(filename_xls)#创建一个book class，打开excel文件
        sh = table.sheet_by_index(0) #获取一个sheet对象
        for line in range(0,sh.nrows):#0-含第一行。nrows = table.nrows #行数 ncols = table.ncols #列数 print sh.row_values(rownum)
            row = sh.row_values(line)
            yield [r for r in row]
    except Exception as ex:
        print('Error execute: {}'.format(ex))
        yield []



# def get_excel_serialNumber(file_excel):
#     x = 1
#     mylist = []
#     while True:
#         try:
#             g = get_excel_x_y(file_excel, x, 0)        
#             x += 1
#             if g == 0 or g != '':
#                 mylist.append(int(g))
#         except Exception as ex:
#             break
#     return mylist        