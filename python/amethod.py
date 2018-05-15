#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:19:48 2017

@author: hwj
"""

import numpoy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("/hwj/yahoo/python/data/A1Benchmark/real_3.csv")
value=data.value
is_anomaly=data.is_anomaly

