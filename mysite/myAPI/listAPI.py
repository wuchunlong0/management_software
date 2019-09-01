# -*- coding: utf-8 -*-
from decimal import *

def get_sum(mylist):
    '''获得列表元素和 返回浮点数字字符串，保留2位小数。[1,2,3] --> '6.00' '''
    return str(Decimal(sum(mylist)).quantize(Decimal('0.00')))




def get_average(mylist):
    '''获得列表元素平均值 返回浮点数字字符串，保留2位小数。[4,3,4] --> '3.67' '''
    return str(Decimal(sum(mylist)*1.0/(len(mylist))).quantize(Decimal('0.00')))


#单元测试
import unittest
class TestFunc(unittest.TestCase):
    def test_get_sum(self):
        self.assertEqual(get_sum([1,2,3]), '6.00')
    def test_get_value(self):
        self.assertEqual(get_average([4,3,4]), '3.67')
