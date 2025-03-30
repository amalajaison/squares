#!/usr/bin/python3
"""
Created on Tue Mar 4 10:15 2025
@author: modestekatotoka
"""
import numpy as np
import time
import sys
import math
from math import sqrt
import matplotlib.pyplot as plt

# load theoretical fields

#simulation data
data=np.transpose(np.loadtxt('xscan_onesheet.out'))
x_sim,bx_sim,by_sim,bz_sim=data
bx_sim=bx_sim*1e9 *3*2# convert to nT
by_sim=by_sim*1e9 *3*2
bz_sim=bz_sim*1e9 *3*2
print('sim data is:',bz_sim)  
print()
#print(type(data))

#target field
data=np.transpose(np.loadtxt('xscan_onesheet_target.out'))
x_target,bx_target,by_target,bz_target=data
bx_target=bx_target*1e9*3*2 # convert to nT
by_target=by_target*1e9*3*2
bz_target=bz_target*1e9*3*2
print()
print('target data is:',bz_target)

#meta data for theoretical field
import json
with open('data.json') as json_file:
    graphdata=json.load(json_file)

#fluxgate measurement data from TRIUMF 11:07 p.m. Friday, March 28, 2025 (CDT)

data_v2= np.genfromtxt('mapping_data_v2.csv',delimiter=',',skip_header = 1)
print('data today is:',data_v2)

positions=data_v2[:,0] #m

x_data=data_v2[:,1]*(100/10) # field(nT)=field(V)*(100 nT/10 V)
y_data=data_v2[:,2]*(100/10)   #nT
z_data=data_v2[:,3]*(100/10)  #nT

#scanning direction along x-axis
'''
fluxgate z-axis direction =  minus x direction in simulation
fluxgate y-axis direction =  minus z-axis direction in simulation
fluxgate x-axis direction =  posi y-axis direction in simulation
'''
    

#measurement
plt.figure()
plt.scatter(-positions,-z_data,color="b",label="$B_x(x,0,0)$",marker='.')
plt.scatter(-positions,-x_data,color="r",label="$B_y(x,0,0)$",marker='.')
plt.scatter(-positions,y_data,color="g",label="$B_z(x,0,0)$",marker='.')


# now plot simulation on top of this
plt.plot(x_sim,bx_sim,color="b",label="$B_x(x,0,0)$")
plt.plot(x_sim,by_sim,color="r",label="$B_y(x,0,0)$")
plt.plot(x_sim,bz_sim,color="g",label="$B_z(x,0,0)$")


plt.plot(x_target,bx_target,'--',color="b",label="$B_x(x,0,0)=%s$"%(graphdata['Pix']))
plt.plot(x_target,by_target,'--',color="r",label="$B_y(x,0,0)=%s$"%(graphdata['Piy']))
plt.plot(x_target,bz_target,'--',color="g",label="$B_z(x,0,0)=%s$"%(graphdata['Piz']))

plt.xlabel("Position along $x$-axis (cm)")
plt.ylabel("Magnetic Field (nT)")


ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]*3
handles=[ph[0]]+h[0:3]+[ph[1]]+h[3:6]+[ph[2]]+h[6:9]
labels=[r'\underline{Measured}']+l[0:3]+[r"\underline{Simulated}"]+l[3:6]+[r"\underline{Target} $(\ell,m)=(%d,%d)$"%(graphdata['l'],graphdata['m'])]+l[6:9]


plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (m)")
plt.ylabel("Magnetic Field (nT)")
plt.legend(handles, labels, ncol=3)


plt.show()

