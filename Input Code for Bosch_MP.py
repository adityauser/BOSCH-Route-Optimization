# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:40:02 2019

@author: Karnika
"""

import os
import xlrd
import xlsxwriter 
Places=[]
book = xlrd.open_workbook(os.path.join("a.xlsx"))
sh = book.sheet_by_name("Sheet1")
i = 0
while True:
    try:
        sp = sh.cell_value(i,0)
        Places.append(sp)
        i = i + 1
    except IndexError:
        break
UP=list(set(Places))
Uni={}
for i in Places:
    if i not in Uni:
        Uni[i]=1
    else:
        Uni[i]=Uni[i]+1
distance_matrix={}
time_matrix={}
for i in range(len(UP)):
    for j in range(len(UP)):
        if i==j:
            distance_matrix[UP[i],UP[j]]=0
            time_matrix[UP[i],UP[j]]=0
        elif i>j :
            distance_matrix[UP[i],UP[j]]=10
            time_matrix[UP[i],UP[j]]=10
            distance_matrix[UP[j],UP[i]]=distance_matrix[UP[i],UP[j]]
            time_matrix[UP[j],UP[i]]=time_matrix[UP[i],UP[j]]
workbook=xlsxwriter.Workbook('Input Data.xlsx')
worksheet=workbook.add_worksheet('distance')
P=1
for i in UP:
    Q=1
    for j in UP:
        a=distance_matrix[i,j]
        worksheet.write(P,Q,a)
        worksheet.write(0,Q,UP[Q-1])
        Q=Q+1
    worksheet.write(P,0,UP[P-1])
    P=P+1
worksheet=workbook.add_worksheet('time')
P=1
for i in UP:
    Q=1
    for j in UP:
        a=time_matrix[i,j]
        worksheet.write(P,Q,a)
        worksheet.write(0,Q,UP[Q-1])
        Q=Q+1
    worksheet.write(P,0,UP[P-1])
    P=P+1
worksheet=workbook.add_worksheet('demand')
P=1
for i in Uni:
    worksheet.write(P,0,i)
    worksheet.write(P,1,Uni[i])
    P=P+1
workbook.close()
        
        
