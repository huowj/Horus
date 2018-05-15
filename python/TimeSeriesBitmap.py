#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 10:08:41 2017

@author: hwj
"""

import csv
import numpy as np


with open("/hwj/yahoo/python/data/A2Benchmark/synthetic_2.csv") as f:
  reader = csv.DictReader(f)
  value = [float(row['value']) for row in reader]
  is_anomaly = [int(row['is_anomaly']) for row in reader]

#inititalize N
N=188
length=len(value)

#matrix initialization
cgr1=mat([['a','b'],
          ['c','d']])
cgr2=mat([['aa','ab','ba','bb'],
          ['ac','ad','bc','bd'],
          ['ca','cb','da','db'],
          ['cc','cd','dc','dd']])
cgr3=mat([['aaa','aab','aba','abb','baa','bab','bba','bbb'],
          ['aac','aad','abc','abd','bac','bad','bbc','bbd'],
          ['aca','acb','ada','adb','bca','bcb','bda','bdb'],
          ['acc','acd','adc','add','bcc','bcd','bdc','bdd'],
          ['caa','cab','cba','cbb','daa','dab','dba','dbb'],
          ['cac','cad','cbc','cbd','dac','dad','dbc','dbd'],
          ['cca','ccb','cda','cdb','dca','dcb','dda','ddb'],
          ['ccc','ccd','cdc','cdd','dcc','dcd','ddc','ddd']])
print(cgr1)
print(cgr2)
print(cgr3)

#bitmap
def cgr_bit(n):
    end=int(N/n)+1
    for i in range(0,end):
        
    