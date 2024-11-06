#!/usr/bin/python3

import numpy as np
import time
import matplotlib.pyplot as plt

# M Katotoka Nov 3,2024
#using global variables: x,y,z for each sensor position.
#the code utilizes the results from M. Zhao's MSR simulation to monitor coils currents.

import csv

#building vec_capitalM Matrix for  M=sc (sensor x coil) 81 x 54

#coils
coil=np.ones(54)
coils=coil.reshape(1,54)
print('coils',coils)

vec_smallm=[] #initizes an empty array pof vec_capitalM

for i in range(54):  # From coilnum00.txt to coilnum54.txt
    file = f"coilnum{i:02d}" 
    
    print(f"Loading data from: {file}.txt")

with open(f'{file}.txt','r') as f:
    lines=f.readlines()
    header=lines[0].strip()
    #print(f"Header line: {header}")
    for line in lines[1:]:
        if line.strip(): # removes empty spaces
            try:
                vec_M=[float(value) for value in line.strip().split()[:3]]
                vec_smallm.append(vec_M)
            except ValueError:
                print(f"skipping invalid line: {line}")

#print(f"vec_smallm:{vec_smallm[:5]}")
#print(f"vec_capitalM is: {vec_capitalM}")

vec_smallm_array=np.array(vec_smallm)
#print('vec_smallm_array',vec_smallm_array)
vec_capitalM=np.transpose(vec_smallm_array)  
#print('vec_capitalM_array_transp',vec_capitalM)

#capital_Mprime=vec_capitalM*coils  #the vec_capitalM matrix, using only one coil for now
#capital_M=capital_Mprime.reshape(81,54)
#print(f"capital_M:{capital_M}")
#print(len(capital_M))

'''
#calculting the invese of the vec_capitalM Matrix.
from numpy.linalg import inv

Minv=inv(capital_M))
print('Minv',Minv)
'''

#Now building vec_B matrix 81 x 1, a vector of magnetic fields, same ordering as above.

vec_smallb=[] #initizes an empty array pof vec_capitalb

for i in range(54): 
    file = f"coilnum{i:02d}"

with open(f'{file}.txt','r') as f:
    lines=f.readlines()
    header=lines[0].strip()
    #print(f"Header line: {header}")
    print()
   
    for line in lines[1:]:
        if line.strip(): # removes empty spaces
            try:
                vec_Bprime=[float(value) for value in line.strip().split()[3:6]]
                vec_smallb.append(vec_Bprime)
            except ValueError:
                print(f"skipping invalid line: {line}")

#print(f"vec_smallb:{vec_smallb[:5]}")
#print(f"vec_capitalBprime is: {vec_capitalBprime}")

vec_smallb_array=np.array(vec_smallb)
print('vec_smallb_array',vec_smallb_array)
vec_BBprime=np.transpose(vec_smallb_array)  
print('vec_capitalB_array_transp',vec_BBprime)

vec_B=vec_BBprime.reshape(81,1) #,  #the vec_B matrix
print(f"capital_M:{vec_B}")
print(len(vec_B))

