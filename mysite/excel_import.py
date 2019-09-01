# -*- coding: UTF-8 -*-
import os
import sys
import django
import random
import datetime

file_excel = 'mysite/bank/files/bank_employe.xlsx'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()

    from bank.models import Bankemploye
    from myAPI.excelAPI import load_excel_model

    '''数据库(Bankemploye)字段'''
    k = ['serialNumber', 'title', 'subitem', 'drivingfactors', 'investigation',\
         'classificationNumber', 'score', 'dimensionalItems', 'remarks']
    
    '''电子表格文件导入数据库(Bankemploye) '''
    load_excel_model(file_excel, Bankemploye, k)