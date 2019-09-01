# -*- coding: utf-8 -*-
import os
from .listdictAPI import  listdictAPI

'''
 L1 = []与 L2 = [''] 区别：L1[0] 出错；L2[0] 不出错 2018.10.28    
>>> [][0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
>>> [''][0]
''
>>> 
'''
import json

def readJson(filepath):
    """读json格式文件"""
    with open(filepath) as fp:        
        return json.load(fp)
   
def writeJson(filepath,myDict):     
    """写json格式文件"""
    ret = True
    try:
        with open(filepath,'w+') as fp:  
            fp.write(json.dumps(myDict))
    except Exception as ex:
        print('Error execute: {}'.format(ex))
        ret = False
    return ret
     
def readline_list(filename):
    """逐行读文本文件（抛弃空行），列表"""
    try:
        with open(filename,'r') as f:
            lines = f.readlines()
            return [l  for l in lines if l.strip()] #抛弃空行 
        return ['']
    except Exception as ex:
        print('Error execute: {}'.format(ex))
        return ['']
        
def readline_txt(filename):
    """逐行读文本文件（抛弃空行），返回字符串"""
    return ''.join(readline_list(filename))  
     
class MyFile:
    def __init__(self, dirpath, extlist):
        self.dirPath = dirpath  
        self.extList = extlist   
        
    def toNameList(self):
        """以列表形式，获得指定目录下，指定类型的全部文件名。extlist ＝［］获得指定目录下,全部目录名、文件名.
        MyFile('bank/static/helpdoc', ['.jpg']).toNameList()
        """
        try:
            """列表形式，返回指定目录下所有的文件和目录名（不含路径的短文件名）"""
            fileNames = os.listdir(self.dirPath)       
        except Exception as ex:
            print('Error execute: {}'.format(ex))
            #raise
            return ['']  # L1 = []与 L2 = [''] 区别：L1[0] 出错；L2[0] 不出错 2018.10.28    
        if (len(self.extList) > 0):
             fileNames = [fileName for fileName in fileNames \
                          if listdictAPI(self.extList, fileName).isListInStr()]
        filepathList = [os.path.join(self.dirPath, i) for i in fileNames 
                    if (not '._' in i)&(not '.DS' in i)]#（含路径的文件名）2016.10.24
        if filepathList == []:
            filepathList = ['']            
        return filepathList
    
    def get_readlineTxt(self):
        """
        逐行获得文本文件内容 
        """
        try:
            filenames = MyFile(self.dirPath,self.extList).toNameList()        
            for f in filenames:
                yield readline_txt(f)
        except Exception as ex:
            print('Error execute: {}'.format(ex))
            yield ''    

    def get_openTxt(self):
        """
        获得文本文件内容,应用在 
        MyFile('bank/static/helpdoc', ['.md']).get_openTxt()
        """
        try:
            filenames = MyFile(self.dirPath,self.extList).toNameList()        
            for f in filenames:
                yield open(f, 'r').read()
        except Exception as ex:
            print('Error execute: {}'.format(ex))
            yield ''    



import zipfile
def zipDir(dirpath, outFullName):
    '''
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName:  压缩文件保存路径+XXXX.zip
    :return: 无
    '''
    zip = zipfile.ZipFile(outFullName, 'w', zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标和路径，只对目标文件夹下边的文件及文件夹进行压缩（包括父文件夹本身）
        this_path = os.path.abspath('.')
        fpath = path.replace(this_path, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()