# -*- coding: utf-8 -*-
'''
   ListDictAPI.py 列表字典类
   
2017.1.16
'''
import json
   
class listdictAPI:
    def __init__(self, myList, myStr):
        self.subStrList = myList
        self.inputStr = myStr


    #判断列表MyList中所有元素,是否都包含在字符串MyStr中。是True、否False
    def isListAllInStr(self):
        return all([i in self.inputStr for i in self.subStrList])

        
    #判断列表MyList中的一个（含）以上元素是否包含在字符串MyStr中。是True、否False
    def isListInStr(self):
        '''
        >>> any(['a', 'b', 'c', 'd'])  #列表list，元素都不为空或0
        True
        >>> any(['a', 'b', '', 'd'])  #列表list，存在一个为空的元素
        True
        >>> any([0, '', False])  #列表list,元素全为0,'',false
        False
        '''       
        return any([i in self.inputStr for i in self.subStrList])
    
    #判断字符串MyStr是否包含在列表MyList中。是True、否False
    def isStrInList(self):
        return any([self.inputStr in i for i in self.subStrList])

def listdictTolists(listdict):
    """转换结果便于保存电子表格"""
    return [[v for d in listdict for k,v in d.items() if k == 'id'],\
            [v for d in listdict for k,v in d.items() if k == 'title'],\
            [v for d in listdict for k,v in d.items() if k == 'sum'],\
            [v for d in listdict for k,v in d.items() if k == 'a'],\
            [v for d in listdict for k,v in d.items() if k == 'b'],\
            [v for d in listdict for k,v in d.items() if k == 'c'],\
            [v for d in listdict for k,v in d.items() if k == 'd'],\
            [v for d in listdict for k,v in d.items() if k == 'e']]        

import unittest            
class TestlistdictAPI(unittest.TestCase):     
    def test_isListAllInStr_all_T(self):
        listdictapi=listdictAPI(['F','EMS','txt'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListAllInStr(),True)                                           
    def test_isListAllInStr_1_F (self):
        listdictapi=listdictAPI(['F1','EMS','txt'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListAllInStr(),False)                                           
    def test_isListAllInStr_2_F (self):
        listdictapi=listdictAPI(['F1','EMS1','txt'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListAllInStr(),False)                                           
    def test_isListAllInStr_3_F(self):
        listdictapi=listdictAPI(['F1','EMS1','txt1'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListAllInStr(),False)                                           
    def test_isListAInStr_1_T (self):
        listdictapi=listdictAPI(['F','EMS1','txt1'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListInStr(),True)                                           
    def test_isListAInStr_2_T (self):
        listdictapi=listdictAPI(['F','EMS','txt1'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListInStr(),True)                                           
    def test_isListAInStr_3_T (self):
        listdictapi=listdictAPI(['F','EMS','txt'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListInStr(),True)                                           
    def test_isListAInStr_all_F(self):
        listdictapi=listdictAPI(['F1','EMS1','txt1'],'F06925EMS91.txt')
        self.assertEquals(listdictapi.isListInStr(),False)  
        
    def test_isStrInList_T (self):
        listdictapi=listdictAPI(['F','EMS','txt'],'M')
        self.assertEquals(listdictapi.isStrInList(),True)                                           
    def test_isStrInList_F(self):
        listdictapi=listdictAPI(['F1','EMS1','txt1'],'1t')
        self.assertEquals(listdictapi.isStrInList(),False)  
        
    def test_listdictTolists(self):
        listdict=[{'e': 6, 'id': 0, 'c': 3, 'b': 6, 'd': 8, 'title': '员工对分行的技术和工具使员工能够成功地开展工作有何评价？', 'a': 7, 'sum': 30},\
              {'e': 9, 'id': 1, 'c': 6, 'b': 2, 'd': 8, 'title': '员工对能够及时获得足够有效的信息以有效地完成工作有何评价？', 'a': 5, 'sum': 30}, \
              {'e': 3, 'id': 2, 'c': 5, 'b': 8, 'd': 5, 'title': '员工在工作中不会经常因为资源配置不足而无法工作有何评价？', 'a': 9, 'sum': 30}, \
              {'e': 5, 'id': 3, 'c': 9, 'b': 4, 'd': 7, 'title': '员工对各级各类信息与知识数据库系统建设有何评价？', 'a': 5, 'sum': 30}]
        
        newlist=[[0, 1, 2, 3],\
             ['员工对分行的技术和工具使员工能够成功地开展工作有何评价？', '员工对能够及时获得足够有效的信息以有效地完成工作有何评价？', '员工在工作中不会经常因为资源配置不足而无法工作有何评价？', '员工对各级各类信息与知识数据库系统建设有何评价？'], \
             [30, 30, 30, 30],\
             [7, 5, 9, 5],\
             [6, 2, 8, 4],\
             [3, 6, 5, 9],\
             [8, 8, 5, 7], \
             [6, 9, 3, 5]]   
        self.assertEquals(listdictTolists(listdict),newlist)