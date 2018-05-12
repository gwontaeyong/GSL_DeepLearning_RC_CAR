# -*- coding: utf-8 -*-
"""
Created on Sun May 13 00:47:38 2018

@author: byebye
"""

import csv

f = open('output.csv', 'r')
rdr = csv.reader(f)
y_data = []
for line in rdr:
    addr = line[0]
    angle = line[1]
    speed = line[2]
    #print(type(angle))
    #print(addr,angle,speed)
    if angle == '0':
        y_data.append([1,0,0,0,0,0])
    elif angle == '1':
        y_data.append([0,1,0,0,0,0])
    elif angle == '2':
        y_data.append([0,0,1,0,0,0])
    elif angle == '3':
        y_data.append([0,0,0,1,0,0])
    elif angle == '4':
        y_data.append([0,0,0,0,1,0])
    elif angle == '5':
        y_data.append([0,0,0,0,0,1])
    
f.close()

print(y_data)
