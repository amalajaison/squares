#!/usr/bin/python3

import numpy as np
import time
import matplotlib.pyplot as plt

# M Katotoka Nov 3,2024
#using global variables: x,y,z for each sensor position.
#the code utilizes the results from M. Zhao's MSR simulation to monitor coils currents.

import csv

#building capitalM Matrix for  M=sc (sensor x coil)


b_prime=np.zeros((81,1)) #initilizes an empty array for magnetic field in three axis for all the coils                 
m=np.zeros((54,81))
#print(np.shape(m),m)

#singular value decomp, svd

U, s, VT=np.linalg.svd(m, full_matrices=True)
#print('s is',s)  #s is a 1D array of a’s singular values

for i in range(54):  # coils from coilnum00 to coilnum53
    file=f"coilnum{i:02d}" 
    print(f"Loading data from: {file}.txt")
    b_coil=np.zeros((81,1))  #magnetic field value for  each coils
    print(np.shape(b_coil),'b for each coil is:',b_coil)
    with open(f'{file}.txt','r') as f:
        lines=f.readlines()
        header=lines[0].strip()
        #print(f"Header line: {header}")
        for line in lines[1:]:
            if line.strip():   #removes any whitespaces at beginning of- and trailing of any string
                values=[float(value) for value in line.strip().split()]
                if len(values)==8: # 3 positions, 3 B-field values, 1 Bmod, and 1 header(should be 8 values)
                    print(f"Skipping lines without correct dimensions:{line.strip()}")
                    continue
                for j in range(27):
                    bx,by,bz=values[3],values[4],values[5]
                    print(f"Coil{file},Sensor{j:02d},Bx:{bx},By:{by},Bz:{bz}")
                    b_coil=[bx,by,bz]
                    print(b_coil)
                    for k in range(3):
                        m[i,j*3+k]=b_coil[k]
                #print(len(b_coil),'b_field final is:',b_coil) # for each coil
print (np.shape(m),'m is ',m)
vec_b=b_coil
print(np.shape(vec_b),'vec_b is ',b_coil)
capital_M=m.T #Transpose of m
print(np.shape(capital_M),'capital_M is ',capital_M)
#print('s is',s)  #s is a 1D array of a’s singular values

vec_i=capital_M.dot(vec_b)
print('vec_i is:',vec_i)

