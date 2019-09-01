# -*- coding: UTF-8 -*-

#字典按键值排序
def dict_sorted(d):
    try:
        return  sorted(d.items(), key = lambda kv:(kv[1], kv[0]))   
    except Exception as ex:
        print('err: %s' %ex) 
        return {} 
  
#单元测试
import unittest
class TestFunc(unittest.TestCase):
    def test_dict_sorted(self):
        d = {'d1':'2.10', 'd2':'4.89', 'd4':'1','d3':'3.2'}
        self.assertEqual(dict_sorted(d),\
                          [('d4', '1'), ('d1', '2.10'), ('d3', '3.2'), ('d2', '4.89')])

    def test_dict_sorted_1(self):
        d = {'d1':'2.10', 'd2':'4.89', 'd4':'1','d103':'3.2'}
        self.assertEqual(dict_sorted(d),\
                          [('d4', '1'), ('d1', '2.10'), ('d103', '3.2'), ('d2', '4.89')])

    def test_dict_sorted_2(self):
        d = {'中国':'2.10', 'd2':'4.89', '美国':'1','d103':'3.2'}
        self.assertEqual(dict_sorted(d),\
            [('\xe7\xbe\x8e\xe5\x9b\xbd', '1'), ('\xe4\xb8\xad\xe5\x9b\xbd', '2.10'), ('d103', '3.2'), ('d2', '4.89')])

    def test_dict_sorted_4(self):
        d = {u'中国':'2.10', 'd2':'4.89', u'美国':'1','d103':'3.2'}
        self.assertEqual(dict_sorted(d),\
            [(u'\u7f8e\u56fd', '1'), (u'\u4e2d\u56fd', '2.10'), ('d103', '3.2'), ('d2', '4.89')])
 

''' 
sorted(d,key=d.__getitem__):   实测不能使用！   

def dict_sorted(d):
    try:
        d1={}
        for k in sorted(d,key=d.__getitem__):
            d1.update({k:d[k]})
        return d1

    except Exception as ex:
        print('err: %s' %ex) 
        return {}        
    #特别注意：中文做键名不能排序！！！
    def test_dict_sorted_d(self):
        d = {'中国':'2.1', 'd2':'4', 'd4':'1','美国':'3.2'}
        self.assertEqual(dict_sorted(d),\
            {'\xe4\xb8\xad\xe5\x9b\xbd': '2.1', 'd4': '1', 'd2': '4', '\xe7\xbe\x8e\xe5\x9b\xbd': '3.2'} )
    
    #特别注意：中文做键名不能排序！！！
    def test_dict_sorted_d1(self):
        d = {u'中国':'2.1', 'd2':'4', 'd4':'1',u'美国':'3.2'}
        self.assertEqual(dict_sorted(d),\
            {'d2': '4', 'd4': '1', u'\u4e2d\u56fd': '2.1', u'\u7f8e\u56fd': '3.2'} )
    #特别注意：纯数字字符做键名不能排序！！！
    def test_dict_sorted_0(self):
        d = {'1':'2.10', '2':'4.89', '4':'0','5':'3.2'}
        self.assertEqual(dict_sorted(d),\
                          {'1': '2.10', '2': '4.89', '5': '3.2', '4': '0'})
'''
