#!/usr/bin/python3

import numpy as np
import time
import matplotlib.pyplot as plt
from dipole import *
from scipy.constants import mu_0, pi
from patchlib.patch import *
from Pis.Pislib import *



'''
M Katotoka - created  Nov 3,2024

Updated Tue Feb 18 7:41pm 2025 - Modeste completed the code that outputs vec_i, using M.Zhao matrices, for any target vec_b (see line 112)
---------------------------
In this code:
1. Initializes a matrix m, of zeros, shape 54 rows x 81 coloumns: rows: coils, : coloumns: B field at each sensor position  (x,y,z)

2.  A for loop loads a file containing matrices for each on the 54 coils, each containing sensor positions (x, y,z), magnetic field at each sensor position and the modulus of the field - M. Zhao's matrices. This gives 81 mmeasurements of field
3. Initializes an empty array of b_coil - magnetic field values a each sensor position, shape 81 rows x 1 column.
4. For each coil, the code
i) loads the files
ii) opens the file and reads the line.
iii) For each line (a list), starting from line 1 to the last line, it extracts sensors positions and their magnetic field values, and bmod, assigns them to a variable called  values, and prints an iterable list of these values.
iv)it then checks that the line is full, containing 8 items ie. 3 sensor pos and 3 b-values, 1 bmod, and 1 header. otherwise, it returns an error message.\
v) in the list values, we slice and extract only the specific values we need corresponding bx,by,bz
vi)then prints these values to comfirm, for each correspoding sensor position.
vii) then it assigns these 3 b fields values to the columns of the  b_coil matrix (initialized above as zeros).
viii) the builds and fills up the matrix m; building rows(i) and columns(j*3+k)
ix) we then contruct the matrix by following  a series of steps from line 70

---------------------------'''
import csv

#building capital_M Matrix for  M=sc (sensor x coil)
                 
m=np.zeros((54,81))
#print(np.shape(m),m)

for i in range(54):  # coils from coilnum00 to coilnum53
    file=f"/Users/modestekatotoka/Desktop/tucan_2024/tucan/modeste_squares/squares/shim-coil-mz-matrix/coilnum{i:02d}" 
    print(f"Loading data from: {file}.txt\n")
    b_coil=np.zeros((81,1))  #magnetic field value for  each coils
    print(np.shape(b_coil),'b for each coil is:',b_coil)
    
    with open(f'{file}.txt','r') as f:
        lines=f.readlines()
        header=lines[0].strip()
        #print(f"Header line: {header}")
        print('printing line')
        print('lines',lines)
        print(type(lines))


        for j, line in enumerate(lines[1:]):
            print(line)
            values=[float(value) for value in line.strip().split()]
            print(type(values),'Values is:',values)
            if len(values)==8: # 3 positions, 3 B-field values, 1 Bmod, and 1 header(should be 8 values)
                print(f"skipping lines without correct dimensions:{line.strip()}")
                continue
            #for j in range(27): #this would print the same value above, 27 times. not what we want.
            bx,by,bz=values[3],values[4],values[5]
            print(f"{file},sensor{j:02d},Bx:{bx},By:{by},Bz:{bz}\n")
            b_coil=[bx,by,bz]
            print(b_coil)
            for k in range(3):
                m[i,j*3+k]=b_coil[k]
print (np.shape(m),'m is ',m)
print()
print()
#Transpose of matrix m, call  is capital_M: M=s x c
capital_M=m.T
print(np.shape(capital_M),'capital_M is: ',capital_M)
print()

#svd
U,s,VT=np.linalg.svd(capital_M)

print('s is',s)  #s is a 1D array of  singular values, a list of the diagonal elements, rather than a matrix
print(type(s))

# now buildin the matrix. 
S=np.zeros(capital_M.shape)
print('S is:',S)
S[:capital_M.shape[1],:capital_M.shape[1]]=np.diag(s)
# Or use "full_matrices=True" in the svd command

# Calculating the inverse on capital_Mq
# list of reciprocals
d=1./s
print('d is:',d)

D=np.zeros(capital_M.shape)
#D=np.zeros(capital_M)
print('D is:',D)

# matrix of recipricols
D[:capital_M.shape[1],:capital_M.shape[1]]=np.diag(d)

# now....inverse of capital_M
Minv=VT.T.dot(D.T).dot(U.T)
print('M inverse is:',Minv)
print(Minv.shape)
#or 
#Minv=np.linalg.pinv(capital_M)
#print(Minv)

#Lets get some current: vec_i: required to set on each coil to realize the desired field
#here vec_b: is the target field. e.g selected by dipole, or G_ellm etc.


#target field
data=np.transpose(np.loadtxt('xscan_onesheet_target.out'))
x_target,bx_target,by_target,bz_target=data
bx_target=bx_target
by_target=by_target
bz_target=bz_target
print()
print('target data is:',bx_target)

#vec_b=bx_target
#vec_i=capital_M.dot(vec_b) # using  I= Minv x B
#print('vec_i is:',vec_i)
#print(np.shape(vec_i))

