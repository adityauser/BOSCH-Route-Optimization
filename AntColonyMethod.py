# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 15:15:46 2019

@author: PRASHANT
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 20:36:52 2019

@author: PRASHANT
"""

from gurobipy import*
import os
import xlrd
import numpy as np
from numpy import inf
from scipy import spatial
import numpy
from sklearn.metrics.pairwise import euclidean_distances
import math
import time
import numpy.ma as ma

iteration = 100
n_ants =36
n_facility = 36         ####### 1 PLUS ACTUAL NO OF FACILITES
#n_cust=35
e=0.5
alpha=2
break_limit=20
beta=2
maximum_distance=200
#maximum_time=7000
maximum_capacity=50
#minimum_capacity=10

start=7
end=3
end_demand=1


n_salesman=2
nc=6            ###ALSO CORRECT LINE 89



facility_name=[]
book = xlrd.open_workbook(os.path.join("Input Data final 2.xlsx"))
sh = book.sheet_by_name("distance")
i = 1
l=0
for i in range(1,n_facility+1):  
    sp = sh.cell_value(i,0)
    
    
    facility_name.append(sp)
distance=[]
a=[]
for i in range(1,n_facility+1):
    distance=[]
    for j in range(1,n_facility+1):
        dist=sh.cell_value(i,j)
        distance.append(dist)
#        b=np.array(distance)
    a.append(distance)
    
final_dist=np.array(a)/1000


#sh = book.sheet_by_name("time")
#tim=[]
#b=[]
#for i in range(1,n_facility+1):
#    tim=[]
#    for j in range(1,n_facility+1):
#        t=sh.cell_value(i,j)
#        tim.append(t)
#        
#    b.append(tim)
#    
#final_time=np.array(b)

sh = book.sheet_by_name("demand")
j=1
demand=[]
for i in range(1,n_facility+1):
    a=sh.cell_value(i,j)
    demand.append(a)
zzz=np.array(demand)
#zzzzzz=final_demand.transpose()
    
    
zx=[]
#
for i in range(n_facility):
    zx.append(i)
zx.sort()
#################################################################
################################################################
abc = zzz[:,np.newaxis]
final_demand=abc.transpose()
pheromne = 0.15*np.ones((n_ants,n_facility))
route_name=[]
for i in range(1,n_salesman+1):
    route_name.append("route"+str(i))
print(route_name)

for i in range(len(route_name)):
    a= np.ones((n_ants,n_facility))
    route_name[i]=a       

demand_satisfied_list=[]

for i in range(1,n_salesman+1):
    demand_satisfied_list.append("demand_satisfied_list"+str(i))
print(demand_satisfied_list)

for i in range(len(demand_satisfied_list)):
    a= []
    demand_satisfied_list[i]=a
    
dist_cov_list=[]
for i in range(1,n_salesman+1):
    dist_cov_list.append("dist_cov_list"+str(i))
for i in range(len(dist_cov_list)):
    a= []
    dist_cov_list[i]=a
    
overall_best_route=[]
for i in range(1,n_salesman+1):
    overall_best_route.append("overall_best_route"+str(i))

for i in range(len(overall_best_route)):
    a= []
    overall_best_route[i]=a

demand_satisfied_array=[]
for i in range(1,n_salesman+1):
    demand_satisfied_array.append("demand_satisfied_array"+str(i))

dist_cov_array=[]
for i in range(1,n_salesman+1):
    dist_cov_array.append("dist_cov_array"+str(i))

    
route_opt=[]
for i in range(1,n_salesman+1):
    route_opt.append("route_opt"+str(i))

no_of_cust_covered = np.zeros((1,n_facility))


factor=1/final_dist    
factor[factor==inf]=0
visibility=factor

overall_dist_min_cost=10000000
cost_matrix=np.zeros((iteration,1))
facility_name=[]
for i in range(1,n_facility+1):
    facility_name.append(i)

start_time = time.time()

for ite in range(iteration):             #iteration

    for Q in range((len(route_name))):
        W=start*np.ones((n_ants,1))
        B=end*np.ones((n_ants,n_facility-1))
        F=np.concatenate((W, B), axis=1)

        route_name[Q]=F
    
   ##    
    for Y in range(len(dist_cov_list)):
        a=[]
        dist_cov_list[Y]=a
      
    for i in range(n_ants):              # no of ants
        
        temp_visibility = np.array(visibility)
        demand_satisfied=0
        distance_covered=0
        time_taken=0
        covered_facilities=[]
        unsatisfied_cust=[]
        satisfied_cust=[]
        temp_no_of_cust_covered=np.array(no_of_cust_covered)
        temp_dem_sat_array=np.array(final_demand)

        for u in range(n_salesman):
            
            satisfied_cust=[]


            for j in range(n_facility-1):
                fac=zx[:]

                
                if distance_covered<maximum_distance and len(covered_facilities)!=len(facility_name)-1 and demand_satisfied<maximum_capacity:
#                    print("a")
                    if j>0:
                       
                        for b1 in covered_facilities:
                            temp_visibility[:,b1]=0
                       
                    demand_satisfied=0
                    distance_covered=0
                    satisfied_cust=[]
                    time_taken=0
                    combine_feature = np.zeros(n_facility)
                    cum_prob = np.zeros(n_facility)
                    cur_loc = int(route_name[u][i,j]-1)
                    temp_visibility[:,cur_loc] = 0
                    p_feature = np.power(pheromne[cur_loc,:],beta)
                    v_feature = np.power(temp_visibility[cur_loc,:],alpha)
                    p_feature = p_feature[:,np.newaxis]
                    v_feature = v_feature[:,np.newaxis]
                    combine_feature = np.multiply(p_feature,v_feature)
                    total = np.sum(combine_feature)
                    if total==0:
                        total=1
                            
                    probs = combine_feature/total
                    
                    
                    cum_prob = np.cumsum(probs)
                    r = np.random.random_sample()
                    if np.all(cum_prob==0):
#                        print("b")
                        facility=end
 #                       print("facility =", facility)
                        route_name[u][i,j+1] = facility
#                        covered_facilities.append(facility-1)
                        
                        break
                    else:
#                        print("b")
                        facility = np.nonzero(cum_prob>r)[0][0]+1
#                        print("facility =", facility)
                        covered_facilities.append(facility-1)
                    route_name[u][i,j+1] = facility
                    for v in range(n_facility-1):
                        
                        distance_covered= distance_covered+final_dist[int(route_name[u][i,v])-1,int(route_name[u][i,v+1])-1]
#                        time_taken= time_taken+final_time[int(route_name[u][i,v])-1,int(route_name[u][i,v+1])-1]
                        satisfied_cust.append(final_demand[0,int(route_name[u][i,v])-1])
                    demand_satisfied=sum(satisfied_cust)
                    
                    demand_satisfied=demand_satisfied+end_demand
#                    print("satisfied cust =", satisfied_cust)
#                    print("demand satisfied =", demand_satisfied)
                    if distance_covered<maximum_distance and demand_satisfied<maximum_capacity: 
                       
#                        print("c")
#                        for k in range(n_facility-1):
#                            satisfied_cust.append(final_demand[0,int(route_name[u][i,k])-1])
                        covered_facilities.append(facility-1) 
                        prashant=covered_facilities[:]
#                        print("length of covered facil =", len(covered_facilities))
                    
                       
                    else:
#                        print("demand satisfied =",demand_satisfied)
#                        print("distance_covered =",distance_covered)
#                        print("time taken =", time_taken)
#                        print("d")
#                        print("dis covered =", distance_covered)
#                        print("length of covered facil =", len(covered_facilities))
                                                
                        distance_covered=0
                        time_taken=0
                        demand_satisfied=0
                        route_name[u][i,j+1]=end
                        for v in range(n_facility-1):
                            distance_covered= distance_covered+final_dist[int(route_name[u][i,v])-1,int(route_name[u][i,v+1])-1]
#                            time_taken= time_taken+final_time[int(route_name[u][i,v])-1,int(route_name[u][i,v+1])-1]
                            
                        satisfied_cust=[]
#                        print("abc")
                        
                        for k in range(n_facility-1):
                               satisfied_cust.append(final_demand[0,int(route_name[u][i,k])-1])
                        demand_satisfied=sum(satisfied_cust) + end_demand
                        
                        
#                        print("demand satisfied =", demand_satisfied)    
                        demand_satisfied_list[u].append(demand_satisfied)
                        dist_cov_list[u].append(distance_covered)
                        
    
                        break
        
        ################### WE CAN CHECK OTHER COMBINATIONS OTHER THAN THE CHOOSEN FACILITY SO THAT WE MAY GET A FACILITY WHICH IF INCLUDED, THE DISTANCE TRAVELLED IS STILL < MAXIMUM DIST. IF NO SUCH COMB IS AVAILABLE THEN BREAK.
        #                    break
                       
                elif (distance_covered<maximum_distance and len(prashant)==(len(facility_name)-1) and demand_satisfied< maximum_capacity):
#                    print("dis covered =", distance_covered)
#                    print("length of covered facil =", len(covered_facilities))
#                    print("e")
                    distance_covered=0
                    time_taken=0
                    route_name[u][i,j+1]=end
                    for v in range(n_facility-1):
                        distance_covered= distance_covered+final_dist[int(route_name[u][i,v])-1,int(route_name[u][i,v+1])-1]
#                        time_taken= time_taken+final_time[int(route_name[u][i,v])-1,int(route_name[u][i,v+1])-1]
                    satisfied_cust=[]
#                    print("g")
#                    print("xyz")
                    for k in range(n_facility-1):
                           satisfied_cust.append(final_demand[0,int(route_name[u][i,k])-1])
                    demand_satisfied=sum(satisfied_cust) + demand_satisfied
                    
                    
                        
                    demand_satisfied_list[u].append(demand_satisfied)
                    Apple=len(set(route_name[u][i]))
                    if Apple!=2:
                        dist_cov_list[u].append(distance_covered)
                    else:
                        dist_cov_list[u].append(0)
                        
    
                    break
#                elif demand_satisfied< minimum_capacity and len(prashant)==(len(facility_name)-1):
##                    print("zxcv")
##                    print("f")
#                    for ll in range(0,u):
#                        dist_cov_list[ll].pop()
#                    for pp in range(0,n_salesman):
#                        dist_cov_list[pp].append(0)
#                    break
                    
    for i in range(len(route_name)):
        route_opt[i]=np.array(route_name[i])
#    demand_satisfied_array=np.array(demand_satisfied_list)
    for i in range(n_salesman):
        demand_satisfied_array[i]=np.array(demand_satisfied_list[i])
    
    for i in range(n_salesman):
        dist_cov_array[i]=np.array(dist_cov_list[i])            
                
    overall_demand_satisfied_list=[sum(x) for x in zip(*demand_satisfied_list)]
    overall_demand_satisfied_array=np.array(overall_demand_satisfied_list)

    overall_dist_satisfied_list=[sum(x) for x in zip(*dist_cov_list)]
    overall_dist_satisfied_array=np.array(overall_dist_satisfied_list)            
    
    if overall_dist_satisfied_array.size==0:
        dist_min_loc=0
        dist_min_cost=0
    else:
        dist_min_loc = minvalpos = np.argmin(ma.masked_where(overall_dist_satisfied_array==0, overall_dist_satisfied_array))
        dist_min_cost = overall_dist_satisfied_array[dist_min_loc]

    
############INITIALISING MIN AND MAX PHEROMONE LEVEL    
    if dist_min_cost < overall_dist_min_cost:
        overall_dist_min_cost=dist_min_cost
        
        for A in range(len(overall_best_route)):
            overall_best_route[A]=route_name[A][dist_min_loc]
            
            
        try:
            maximum_pheromne=1/(e* overall_dist_min_cost)
        except ZeroDivisionError:
            maximum_pheromne=0
            
        minimum_pheromne=maximum_pheromne/5

    
######LOCAL PHEROMNE UPDATE    
    pheromne = (1-e)*pheromne
    for c in range(n_ants):
        for v in range(n_facility-1):
            try:
                dt = 1/overall_dist_satisfied_array[c]
                if dt==inf:
                    dt=0
#                print("dt =", dt)

            except IndexError:
                pppp=0
                dt=0
            for B in range(n_salesman):
                pheromne[int(route_opt[B][c,v])-1,int(route_opt[B][c,v+1])-1] = pheromne[int(route_opt[B][c,v])-1,int(route_opt[B][c,v+1])-1] + dt
#            print(pheromne)
    
    
    
######GLOBAL PHEROMONE UPDATE   
    for B in range(n_salesman):            
        for c in range(n_facility-1):        
            pheromne[int(overall_best_route[B][c])-1,int(overall_best_route[B][c+1])-1]=pheromne[int(overall_best_route[B][c])-1,int(overall_best_route[B][c+1])-1]+dt
#    print("@@@@@@@@@@@@@@@@@#######################")
#    print(pheromne)
          
###### MAXIMUM AND MIN LIMIT ON PHEROMNE    
    for B in range(n_salesman):        
        for c in range(n_ants):
            for v in range(n_facility):    
                if pheromne[c,v]<minimum_pheromne:
                    pheromne[c,v]=minimum_pheromne
                if pheromne[c,v]>maximum_pheromne:
                    pheromne[c,v]=maximum_pheromne
final_distance=0
for C in range(n_salesman):
    for v in range(n_facility-1):
        
        final_distance+= final_dist[int(overall_best_route[C][v])-1,int(overall_best_route[C][v+1])-1]
total_time=time.time() - start_time    
#print('route of all the ants at the end :')
#print(route_opt)
print()
print('best path :',overall_best_route)
#print('cost of the best path',int(dist_min_cost[0]) + fac_dist[int(best_route[-2])-1,0])  
#print('maximum demand satisfied =',overall_max_satisfied_cust)        
print("total distance covered =",final_distance)
print("total time taken =",total_time) 

