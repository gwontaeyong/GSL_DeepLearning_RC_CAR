# -*- coding: utf-8 -*-
"""
Created on Sun May 13 00:47:38 2018

@author: byebye
"""

import csv

f = open('output.csv', 'r')
rdr = csv.reader(f)

for line in rdr:
    addr = line[0]
    angle = line[1]
    speed = line[2]
    print(addr,angle,speed)    
f.close()