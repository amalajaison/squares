#!/usr/bin/python3

import numpy as np
import time
import matplotlib.pyplot as plt

# M Katotoka Nov 3,2024
#using global variables: x,y,z for each sensor position.
#the code utilizes the results from M. Zhao's MSR simulation to monitor coils currents.

import csv

#building vec_capitalM Matrix for  M=sc (sensor x coil)

import numpy as np

sensors=np.float64((
    (-0.25, -0.25, -0.25),
    (-0.25, -0.25,  0),
    (-0.25, -0.25,  0.25),
    (-0.25,  0,   -0.25),
    (-0.25,  0,    0),
    (-0.25,  0,    0.25),
    (-0.25,  0.25, -0.25),
    (-0.25,  0.25,  0),
    (-0.25,  0.25,  0.25),
    ( 0,   -0.25, -0.25),
    ( 0,   -0.25,  0),
    ( 0,   -0.25,  0.25),
    ( 0,    0,   -0.25),
    (0, 0, 0),
    (0,   0,   0.25),
    ( 0,    0.25, -0.25),
    (0,   0.25, 0),
    (0,   0.25, 0.25),
    ( 0.25, -0.25, -0.25),
    ( 0.25, -0.25,  0),
    ( 0.25, -0.25,  0.25),
    ( 0.25,  0,   -0.25),
    (0.25, 0,   0),
    (0.25, 0,   0.25),
    ( 0.25,  0.25, -0.25),
    (0.25, 0.25, 0.25)
))


print('sensors_xyz:',sensors)

vec_smallm=[] #initizes an empty array pof vec_capitalM

#building shape and size of matrix

coils=np.ones((54,1))
#print(np.shape(coils),coils)
                   
m=np.zeros((54,81))
print(np.shape(m),m)

capital_M=np.transpose(m) #Transpose of m
print(np.shape(capital_M),'capital_M',capital_M)

#singular value decomp, svd

U, s, VT = np.linalg.svd(capital_M, full_matrices=True)
#print('s is',s)  #s is a 1D array of a’s singular values

for i in range(54):  # coils from 0 to 53
    file=f"coilnum{i:02d}" 
    print(f"Loading data from: {file}.txt")
    with open(f'{file}.txt','r') as f:
        lines=f.readlines()
        header=lines[0].strip()
        #print(f"Header line: {header}")
        for line in lines[1:]:
            if line.strip(): # removes empty spaces
                try:
                    for j in range(81):
                         #sensors=[float(value) for value in line.strip().split()[0:3]]]
                         b_prime=[float(value) for value in line.strip().split()[:3]]
                         print('b_prime is:',b_prime)
                         r=sensors[j]
                         bx,by,bz=coils[i].b_prime(r[0],r[1],r[2])
                         b=[bx,by,bz]
                         for k in range(3):
                    #vec_M=[float(value) for value in line.strip().split()[:3]]
                            m[i,j*3+k]=b[k]
                    #vec_smallm.append(vec_M)
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
print(f"capital_B:{vec_B}")
print(len(vec_B))
'''
