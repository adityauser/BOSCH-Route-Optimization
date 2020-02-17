# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 03:02:36 2019

@author: Karnika
"""
import googlemaps 
#import xlsxwriter  
# Requires API key 
gmaps = googlemaps.Client(key='AIzaSyAv_csn_X3baOtMroij9osCuFaMa8X7lOA') 
  
# Requires cities name 
my_dist = gmaps.distance_matrix('Devegowda Petrol Bunk','Hoskeralli')['rows'][0]['elements'][0] 
  
# Printing the result 
print(my_dist)
a=my_dist['distance']['value']
b=my_dist['duration']['value']
print(a,b)
#workbook=xlsxwriter.Workbook('Result.xlsx')
#worksheet=workbook.add_worksheet('Result')
#f=my_dist
#worksheet.write(0,0,f)
#workbook.close()