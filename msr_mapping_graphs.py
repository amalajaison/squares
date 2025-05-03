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
bx_sim=bx_sim*1e9 *3# convert to nT
by_sim=by_sim*1e9 *3
bz_sim=bz_sim*1e9 *3
#print('sim data is:',bz_sim)  
print()
#print(type(data))

#simulation with rough factor of 2
bx_sim_app=bx_sim*2 # convert to nT
by_sim_app=by_sim*2
bz_sim_app=bz_sim*2

#target field
data=np.transpose(np.loadtxt('xscan_onesheet_target.out'))
x_target,bx_target,by_target,bz_target=data
bx_target=bx_target*1e9*3 # convert to nT
by_target=by_target*1e9*3
bz_target=bz_target*1e9*3
print()
#print('target data is:',bz_target)

#target data with rough approximation of 2
bx_target_app=bx_target*2 # convert to nT
by_target_app=by_target*2
bz_target_app=bz_target*2

#load COMSOL xscan_comsol.txt data for G10

data_com= np.loadtxt('xscan_comsol.txt',delimiter=None,comments='%',skiprows=6)
#print('comsol',data_com)
#print(len(data_com))
pos_com=data_com[:,0] # in m
bx_com=data_com[:,3]*3*(10**9)
by_com=data_com[:,4]*3*(10**9)
bz_com=data_com[:,5]*3*(10**9)#nT
print(by_com)



#meta data for theoretical field
import json
with open('data.json') as json_file:
    graphdata=json.load(json_file)

#fluxgate measurement data from TRIUMF 11:07 p.m. Friday, March 28, 2025 (CDT)

data_v2= np.genfromtxt('mapping_data_v2.csv',delimiter=',',skip_header = 1)
#print('data today is:',data_v2)

positions=data_v2[:,0] #m

x_data=data_v2[:,1]*(100/10) # field(nT)=field(V)*(100 nT/10 V)
y_data=data_v2[:,2]*(100/10)   #nT
z_data=data_v2[:,3]*(100/10)  #nT

print(len(x_data),'x_data is:',x_data)

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
plt.plot(x_sim,by_sim,color="orange",label="$B_y$")
plt.plot(x_sim,bz_sim,color="orange",label="$B_z$")


plt.plot(x_target,bx_target,'--',color="b",label="$B_x(x,0,0)=%s$"%(graphdata['Pix']))
plt.plot(x_target,by_target,'--',color="orange",label="$B_y=%s$"%(graphdata['Piy']))
plt.plot(x_target,bz_target,'--',color="orange",label="$B_z=%s$"%(graphdata['Piz']))


# now plot simulation with factor of 2: image current effects
plt.plot(x_sim,bx_sim_app,color="black",label="$B_x(x,0,0)$")
plt.plot(x_sim,by_sim_app,'--',color='orange',label="$B_y$")
plt.plot(x_sim,bz_sim_app,'--',color='orange',label="$B_z$")


# now plot target with factor of 2
plt.plot(x_target,bx_target_app,'--',color="black")
plt.plot(x_target,by_target_app, color='orange')
plt.plot(x_target,bz_target_app, color='orange')

# band showing theory approximation, most likely  between simulated fields
# for simulation
plt.fill_between(x_sim,bx_sim,bx_sim_app,facecolor='gray',alpha=0.5)
plt.fill_between(x_sim,by_sim,by_sim_app,facecolor='gray',alpha=0.5)
plt.fill_between(x_sim,bz_sim,bz_sim_app,facecolor='gray',alpha=0.5)

#COMSOL result

plt.plot(pos_com,bx_com,color="magenta",label="$B_x(x,0,0)$")
plt.plot(pos_com,by_com, color='orange',label="$B_y$")
plt.plot(pos_com,bz_com, color='orange',label="$B_z$")

plt.axhline(0, color='orange', linestyle='--')



plt.xlabel("Position along $x$-axis (m)",fontsize=12)
plt.ylabel("Magnetic Field (nT)",fontsize=12)


ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]*5
handles=[ph[0]]+h[0:3]+[ph[1]]+h[3:6]+[ph[2]]+h[6:9]+[ph[3]]+h[9:12]+[ph[4]]+h[12:15]
labels=[r'\underline{Measured}']+l[0:3]+[r"\underline{Simulated: In free space}"]+l[3:6]+[r"\underline{Target} $(\ell,m)=(%d,%d)$"%(graphdata['l'],graphdata['m'])]+l[6:9]+[r"\underline{Image current effects: $\approx$ a factor of 2}"]+l[9:12]+[r"\underline{COMSOL}"]+l[12:15]

plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (m)")
plt.xlim([-1.1,1.1])
plt.ylim([-40,40])
plt.ylabel("Magnetic Field (nT)")
plt.legend(handles, labels, ncol=5,fontsize=12)

plt.savefig("/Users/modestekatotoka/Desktop/uwinnipeg_2024/Honour's thesis/mapping_data_analysis/map_my_shims_all.png",dpi=300)

plt.show()
