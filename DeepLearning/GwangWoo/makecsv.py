# -*- coding: utf-8 -*-
"""
Created on Sat May 12 22:31:49 2018

@author: byebye
"""
import csv
import os
f = open('output.csv', 'w', newline='')
wr = csv.writer(f)

def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.jpg': 
                    temp = full_filename.split("_")
                    #print(temp)
                    angle = temp[3]
                    temp2 = temp[4].split(".")
                    speed = temp2[0]
                    wr.writerow([full_filename,angle,speed])
    except PermissionError:
        pass
search("d:/DeepLearning/")          # 전역변수 <-- 이미지있는 상위 폴더 주소
                                    # Tools - Preferences - current working directory 값 잡아준대에 csv파일 저장됨.
f.close()
