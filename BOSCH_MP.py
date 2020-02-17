# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 01:02:42 2019

@author: Karnika
"""

from gurobipy import*
import os
import xlrd
from scipy import spatial
from sklearn.metrics.pairwise import euclidean_distances

book = xlrd.open_workbook(os.path.join("Input Data.xlsx"))

N=[]
Demand={}
co={}
cij={}
K=['V1','V2'] 
Cap = 36
distance=59.2*1000
time=48000
sh = book.sheet_by_name("demand")
i = 1
while True:
    try:
        sp = sh.cell_value(i,0)
        N.append(sp)
        Demand[sp]=sh.cell_value(i,1)        
        i = i + 1
        
    except IndexError:
        break
N_Dash=N[1:]
sh = book.sheet_by_name("distance")    
dij={}

i = 1
for P in N:
    j = 1
    for Q in N:
        dij[P,Q] = sh.cell_value(i,j)
        j += 1
    i += 1
sh = book.sheet_by_name("time")    
tij={}

i = 1
for P in N:
    j = 1
    for Q in N:
        tij[P,Q] = sh.cell_value(i,j)
        j += 1
    i += 1

        
m=Model("Bosch Route Optimization")

m.modelSense=GRB.MINIMIZE

xijk = m.addVars(N,N,K, vtype=GRB.BINARY    ,name='X_ij' )
zik  = m.addVars(N,K,   vtype=GRB.INTEGER   ,name='Z_ik' )
U_ik = m.addVars(N,K,   vtype=GRB.CONTINUOUS,name='U_ik' )


m.setObjective(sum(dij[i,j]*xijk[i,j,k] for i in N for j in N for k in K if i!=j))
for k in K :
    m.addConstr(sum(xijk['Yelachenahalli metro Station',j,k] for j in N )==1)
for k in K:
    m.addConstr(sum(xijk[i,'Bosch Bidadi',k] for i in N   )==1)
for i in N:
    for k in K:
        if i != 'Yelachenahalli metro Station' and i!= 'Bosch Bidadi':
            m.addConstr(sum(xijk[i,j,k] for j in N  if j!=i )==zik[i,k]) 
            m.addConstr(sum(xijk[j,i,k] for j in N  if i!=j )==zik[i,k]) 
        
for i in N_Dash:
    m.addConstr(sum(zik[i,k] for k in K) ==1)
    
for k in K:
    m.addConstr(sum(xijk[i,j,k]*dij[i,j] for i in N for j in N if i!=j)<=distance)
    m.addConstr(sum(xijk[i,j,k]*tij[i,j] for i in N for j in N if i!=j)<=time)

         
for i in N_Dash:
    for j in N:
        for k in K:
            m.addConstr(U_ik[i,k] - U_ik[j,k] + Cap*xijk[i,j,k] <= Cap - Demand[j]) 

for i in N_Dash:
    for k in K:
        m.addConstr(U_ik[i,k] <= Cap) and m.addConstr(U_ik[i,k] >= Demand[i]) 
        
m.write('BOSCH.lp')
m.optimize()
                                            
for v in m.getVars():
    if v.x > 0.01:
        print(v.varName, round(v.x,0))
print('Objective:',m.objVal)



