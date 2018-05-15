#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 20:23:25 2017

@author: hwj
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt

filename="/hwj/yahoo/python/python/data/A1Benchmark/real_5.csv"

data=pd.read_csv("/hwj/yahoo/python/data/A1Benchmark/real_5.csv")

#with open("/hwj/yahoo/python/data/A1Benchmark/real_5.csv") as csvfile:
#    reader=csv.DictReader(csvfile)
#    value=[row['value'] for row in reader]
#with open("/hwj/yahoo/python/data/A1Benchmark/real_5.csv") as csvfile:
#    reader=csv.DictReader(csvfile)
#    is_anomaly=[row['is_anomaly'] for row in reader]
    
def plot(value,is_anomaly):
    x=range(len(value))
    plt.figure(1)
    plt.plot(x,value)
    for i in x:
        if is_anomaly[i]==1:
            plt.plot(i,value[i],'ro-')
    
if __name__ == "__main__":
    plot(data.value,data.is_anomaly)