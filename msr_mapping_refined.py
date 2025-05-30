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
bx_sim=bx_sim*1e9*3  #convert to nT and 3 turns of wires
by_sim=by_sim*1e9*3 
bz_sim=bz_sim*1e9*3 
#print('sim data is:',bz_sim)  
print()
#print(type(data))

#simulation with rough factor of 2, for image current effects
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
#print(by_com)

#meta data for theoretical field
import json
with open('data.json') as json_file:
    graphdata=json.load(json_file)

#fluxgate measurement data from TRIUMF  April 3, 2025

import csv
import numpy as np

data= np.loadtxt('G10_Apr3.csv', delimiter=',', skiprows=19, usecols=(1,2,3,7))
print(data)
bx=data[:,0]
by=data[:,1]
bz=data[:,2]
pos=data[:,3]
#print('pos is:',pos)

'''
print((bx[1]-bx[0])/2)
print((bx[3]-bx[2])/2)
print((bx[5]-bx[4])/2)
print((bx[7]-bx[6])/2)

'''

#bx_ave=[]
bx_ave=np.empty(0, dtype='float64')
for i in range(0, len(bx)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    x_ave=(bx[i+1] - bx[i]) / 2
    #print(x_ave)
    bx_ave=np.append(bx_ave,x_ave)
print('bx_ave is:',bx_ave)
print()
by_ave=np.empty(0, dtype='float64')
for i in range(0, len(by)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    y_ave=(by[i+1] - by[i]) / 2
    #print(y_ave)
    by_ave=np.append(by_ave,y_ave)
print('by_ave is:',by_ave)
print()
bz_ave=np.empty(0, dtype=np.float64)
for i in range(0, len(bz)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    z_ave=(bz[i+1] - bz[i]) / 2
    #print(z_ave)
    bz_ave=np.append(bz_ave,z_ave)
print('bz_ave is:',bz_ave)
print()
positions=np.empty(0, dtype='float64')
for i in range(0, len(pos), 2): 
    position=pos[i]*(0.01) #in m
    #print(position)
    positions=np.append(positions,position)

print(len(positions),'positions is:',positions)

x_data=bx_ave*(100/10) # field(nT)=field(V)*(100 nT/10 V)
y_data=by_ave*(100/10)
z_data=bz_ave*(100/10)

print(len(x_data),'x_data is:',x_data)

# COMSOL all coils

data_com= np.loadtxt('xscan_comsol.txt',delimiter=None,comments='%',skiprows=6) #all coils_comsol
#print('comsol',data_com)
#print(len(data_com))
pos_com_all=data_com[:,0] # in m
bx_com_all=data_com[:,3]*3*(10**9)
by_com_all=data_com[:,4]*3*(10**9)
bz_com_all=data_com[:,5]*3*(10**9)#nT
print(by_com_all)

# coil 4 fluxgate meausurement April 3, 2025
print('Coil 4 data')
data4= np.loadtxt('coil4_Apr3.csv', delimiter=',', skiprows=19, usecols=(1,2,3,7))
print(data)
bx=data4[:,0]
by=data4[:,1]
bz=data4[:,2]
pos=data4[:,3]
#print('pos is:',pos)

bx_ave4=np.empty(0, dtype='float64')
for i in range(0, len(bx)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    x_ave4=(bx[i] - bx[i+1]) / 2
    #print(x_ave4)
    bx_ave4=np.append(bx_ave4,x_ave4)
print('bx_ave for coil 4 is:',bx_ave4)
print()
by_ave4=np.empty(0, dtype='float64')
for i in range(0, len(by)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    y_ave4=(by[i] - by[i+1]) / 2
    #print(y_ave4)
    by_ave4=np.append(by_ave4,y_ave4)
print('by_ave for coil 4 is:',by_ave4)
print()
bz_ave4=np.empty(0, dtype='float64')
for i in range(0, len(bz)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    z_ave4=(bz[i] - bz[i+1]) / 2
    #print(z_ave4)
    bz_ave4=np.append(bz_ave4,z_ave4)
print('bz_ave for coil 4 is:',bz_ave4)
print()

x_data4=bx_ave4*(100/10) # field(nT)=field(V)*(100 nT/10 V)
y_data4=by_ave4*(100/10)
z_data4=bz_ave4*(100/10)

#load coil 4 COMSOL  data G10

data_com= np.loadtxt('bx_on_x_comsol',delimiter=None,comments='%',skiprows=6)  #coil 4 comsol
#print('comsol',data_com)
#print(len(data_com))
pos_com_4=data_com[:,0] # in m
bx_com_4=data_com[:,1]*3 
#by_com_4=data_com[:,4]*3
#bz_com_4=data_com[:,5]*3#nT
print(bx_com_4)


# coil 22 fluxgate meausurement April 3, 2025

print('Coil 22 data')
data22= np.loadtxt('coil22_Apr3.csv', delimiter=',', skiprows=19, usecols=(1,2,3,7))
print(data)
bx=data22[:,0]
by=data22[:,1]
bz=data22[:,2]
pos=data22[:,3]
#print('pos is:',pos)

bx_ave22=np.empty(0, dtype='float64')
for i in range(0, len(bx)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    x_ave22=(bx[i+1] - bx[i]) / 2
    #print(x_ave22)
    bx_ave22=np.append(bx_ave22,x_ave22)
print('bx_ave for coil 22 is:',bx_ave22)
print()
by_ave22=np.empty(0, dtype='float64')
for i in range(0, len(by)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    y_ave22=(by[i+1] - by[i]) / 2
    #print(y_ave22)
    by_ave22=np.append(by_ave22,y_ave22)
print('by_ave for coil 22 is:',by_ave22)
print()
bz_ave22=np.empty(0, dtype='float64')
for i in range(0, len(bz)-1, 2):  # Start at 0, stop at len(bx)-1, step by 2
    z_ave22=(bz[i+1] - bz[i]) / 2
    #print(z_ave22)
    bz_ave22=np.append(bz_ave22,z_ave22)
print('bz_ave for coil 22 is:',bz_ave22)
print()

x_data22=bx_ave22*(100/10) # field(nT)=field(V)*(100 nT/10 V)
y_data22=by_ave22*(100/10)
z_data22=bz_ave22*(100/10)

'''
scanning direction along x-axis

fluxgate z-axis direction =  x direction in simulation
fluxgate minus y-axis direction =  y-axis direction in simulation
fluxgate x-axis direction =  posi z-axis direction in simulation
'''


#Now plots

# measurement all coils:
plt.figure(1)

plt.scatter(-positions,z_data,color="b",label="$B_x(x,0,0)$",marker='.')
plt.scatter(-positions,-y_data,color="r",label="$B_y(x,0,0)$",marker='.')
plt.scatter(-positions,x_data,color="g",label="$B_z(x,0,0)$",marker='.')

ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]
handles=[ph[0]]+h[0:3]
labels=[r'\underline{Measured}']+l[0:3]

plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (m)")
plt.xlim([-1.1,1.1])
plt.ylim([-35,35])
plt.ylabel("Magnetic Field (nT)")
plt.legend(handles, labels, ncol=1, fontsize=14)

plt.savefig("map_my_shims_measured_all.png",dpi=300,bbox_inches='tight')

plt.show()

#comparison to models

plt.figure(2)

plt.scatter(-positions,z_data,color="b",label="$B_x(x,0,0)$",marker='.')
plt.scatter(-positions,-y_data,color="r",label="$B_y(x,0,0)$",marker='.')
plt.scatter(-positions,x_data,color="g",label="$B_z(x,0,0)$",marker='.')

# now plot simulation on top of this

plt.plot(x_sim,bx_sim,color="b",label="$B_x(x,0,0)$")
plt.plot(0,0,color="none",label=' ')
plt.plot(0,0,color="none",label=' ')

#plt.plot(x_sim,by_sim,color="r",label="$B_y(x,0,0)$")
#plt.plot(x_sim,bz_sim,color="g",label="$B_z(x,0,0)$")

#target plot

plt.plot(x_target,bx_target,'--',color="b",label="$B_x(x,0,0)=%s$"%(graphdata['Pix']))
plt.plot(0,0,color="none",label=' ')
plt.plot(0,0,color="none",label=' ')


#plt.plot(x_target,by_target,'--',color="r",label="$B_y(x,0,0)=%s$"%(graphdata['Piy']))
#plt.plot(x_target,bz_target,'--',color="g",label="$B_z(x,0,0)=%s$"%(graphdata['Piz']))


#image current effects

plt.plot(x_sim,bx_sim_app,color="purple",label="$B_x(x,0,0)$")
plt.plot(0,0,color="none",label=' ')
plt.plot(0,0,color="none",label=' ')


#plt.plot(x_sim,by_sim_app,'--',color='r',label="$B_y(x,0,0)$")
#plt.plot(x_sim,bz_sim_app,'--',color='g',label="$B_z(x,0,0)$")


#grey band showing theory approximation

plt.fill_between(x_sim,bx_sim,bx_sim_app,facecolor='gray',alpha=0.12)
#plt.fill_between(x_sim,by_sim,by_sim_app,facecolor='gray',alpha=0.12)
#plt.fill_between(x_sim,bz_sim,bz_sim_app,facecolor='gray',alpha=0.12)

#COMSOL result

plt.plot(pos_com_all,bx_com_all,color="magenta",label="$B_x(x,0,0)$")
plt.plot(0,0,color="none",label=' ')
plt.plot(0,0,color="none",label=' ')


#plt.plot(0,0, color='orange',label="$B_y$")
#plt.plot(0,0, color='brown',label="$B_z$")

#plt.axhline(0, color='orange', linestyle='--')


plt.xlabel("Position along $x$-axis (m)",fontsize=16)
plt.ylabel("Magnetic Field (nT)",fontsize=16)


ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]*5
handles=[ph[0]]+h[0:3]+[ph[1]]+h[3:6]+[ph[2]]+h[6:9]+[ph[3]]+h[9:12]+[ph[4]]+h[12:15]
labels=[r'\underline{Measured}']+l[0:3]+[r"\underline{Free space}"]+l[3:6]+[r"\underline{Target} $(\ell,m)=(%d,%d)$"%(graphdata['l'],graphdata['m'])]+l[6:9]+[r"\underline{Image current effects}"]+l[9:12]+[r"\underline{COMSOL}"]+l[12:15]


plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (m)")
plt.xlim([-1.1,1.1])
plt.ylim([-40,40])
plt.ylabel("Magnetic Field (nT)")
plt.legend(handles, labels, ncol=5,fontsize=13)

#plt.savefig("map_my_shims_models.png",dpi=300)

plt.show()


#measurement for coil 4
plt.figure(3)

plt.scatter(positions,z_data4,color="b",label="$B_x(x,0,0)$",marker='.')
#plt.scatter(positions,-y_data4,color="r",label="$B_y(x,0,0)$",marker='.')
#plt.scatter(positions,x_data4,color="g",label="$B_z(x,0,0)$",marker='.')



ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]
handles=[ph[0]]+h[0:3]
labels=[r'\underline{Measured} ($\ell, m$)=($1,0$)']+l[0:3]

plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (m)")
plt.xlim([-1.1,1.1])
plt.ylim([-60,60])
plt.ylabel("Coil $4$ Magnetic Field (nT)")
plt.legend(handles, labels, ncol=1,fontsize=14)

plt.savefig("map_my_shims_coil4.png",dpi=300,bbox_inches='tight')

plt.show()

#comparison to models: coil 4

plt.figure(4)

plt.scatter(positions,z_data4,color="b",label="$B_x(x,0,0)$",marker='.')
#plt.scatter(0,0,color="r",label="$B_y(x,0,0)$",marker='.')
#plt.scatter(0,0,color="g",label="$B_z(x,0,0)$",marker='.')

#plt.scatter(positions,z_data4,color="b",label="$B_x(x,0,0)$",marker='.')
#plt.scatter(positions,-y_data4,color="r",label="$B_y(x,0,0)$",marker='.')
#plt.scatter(positions,x_data4,color="g",label="$B_z(x,0,0)$",marker='.')


# now plot simulation on top of this

plt.plot(x_sim,bx_sim,color="b",label="$B_x(x,0,0)$")
#plt.plot(x_sim,by_sim,color="r",label="$B_y(x,0,0)$")
#plt.plot(x_sim,bz_sim,color="g",label="$B_z(x,0,0)$")

#target plot

#plt.plot(x_target,bx_target,'--',color="b",label="$B_x(x,0,0)=%s$"%(graphdata['Pix']))
#plt.plot(x_target,by_target,'--',color="r",label="$B_y(x,0,0)=%s$"%(graphdata['Piy']))
#plt.plot(x_target,bz_target,'--',color="g",label="$B_z(x,0,0)=%s$"%(graphdata['Piz']))


#image current effects

plt.plot(x_sim,bx_sim_app,color="purple",label="$B_x(x,0,0)$")
#plt.plot(x_sim,by_sim_app,'--',color='r',label="$B_y(x,0,0)$")
#plt.plot(x_sim,bz_sim_app,'--',color='g',label="$B_z(x,0,0)$")


#grey band

plt.fill_between(x_sim,bx_sim,bx_sim_app,facecolor='gray',alpha=0.12)
#plt.fill_between(x_sim,by_sim,by_sim_app,facecolor='gray',alpha=0.12)
#plt.fill_between(x_sim,bz_sim,bz_sim_app,facecolor='gray',alpha=0.12)

#COMSOL result

plt.plot(pos_com_4,bx_com_4,color="magenta",label="$B_x(x,0,0)$")
#plt.plot(0,0, color='orange',label="$B_y(x,0,0)$")
#plt.plot(0,0, color='orange',label="$B_z(x,0,0)$")

#plt.axhline(0, color='orange', linestyle='--')


plt.xlabel("Position along $x$-axis (m)",fontsize=12)
plt.ylabel("Coil $4$ Magnetic Field (nT)",fontsize=12)


ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]*4
handles=[ph[0]]+h[0:1]+[ph[1]]+h[1:2]+[ph[2]]+h[2:3]+[ph[3]]+h[3:4]
labels=[r'\underline{Measured}']+l[0:1]+[r"\underline{Free space}"]+l[1:2]+[r"\underline{Image current effects}"]+l[2:3]+[r"\underline{COMSOL}"]+l[3:4]


plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (m)")
#plt.xlim([-1.1,1.1])
#plt.ylim([-505,0.1])
plt.ylabel("Coil $4$ Magnetic Field (nT)")
plt.legend(handles, labels, ncol=4,fontsize=14)

plt.savefig("map_my_shims_coil4_models.png",bbox_inches='tight',dpi=300)

plt.show()


#measurement for coil 22
plt.figure(5)

plt.scatter(-positions,z_data22,color="b",label="$B_x(x,0,0)$",marker='.')
plt.scatter(-positions,-y_data22,color="r",label="$B_y(x,0,0)$",marker='.')
plt.scatter(-positions,x_data22,color="g",label="$B_z(x,0,0)$",marker='.')

ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]
handles=[ph[0]]+h[0:3]
labels=[r'\underline{Measured} ($\ell, m$)=($1,0$)']+l[0:3]

plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (m)")
plt.xlim([-1.1,1.1])
plt.ylim([-35,35])
plt.ylabel("Coil $22$ Magnetic Field (nT)")
plt.legend(handles, labels, ncol=1,fontsize=14)

plt.savefig("map_my_shims_coil22.png",dpi=300,bbox_inches='tight')

plt.show()

#comparison to models: coil 22

plt.figure(6)

plt.scatter(-positions,z_data22,color="b",label="$B_x(x,0,0)$",marker='.')
plt.scatter(-positions,-y_data22,color="r",label="$B_y(x,0,0)$",marker='.')
plt.scatter(-positions,x_data22,color="g",label="$B_z(x,0,0)$",marker='.')

# now plot simulation on top of this
plt.plot(x_sim,bx_sim,color="b",label="$B_x(x,0,0)$")
plt.plot(x_sim,by_sim,color="r",label="$B_y(x,0,0)$")
plt.plot(x_sim,bz_sim,color="g",label="$B_z(x,0,0)$")

#target
#plt.plot(x_target,bx_target,'--',color="b",label="$B_x(x,0,0)=%s$"%(graphdata['Pix']))
#plt.plot(x_target,by_target,'--',color="r",label="$B_y(x,0,0)=%s$"%(graphdata['Piy']))
#plt.plot(x_target,bz_target,'--',color="g",label="$B_z(x,0,0)=%s$"%(graphdata['Piz']))


#now plot simulation with factor of 2: image current effects
plt.plot(x_sim,bx_sim_app,color="purple",label="$B_x(x,0,0)$")
plt.plot(x_sim,by_sim_app,'--',color='r',label="$B_y(x,0,0)$")
plt.plot(x_sim,bz_sim_app,'--',color='g',label="$B_z(x,0,0)$")


# now plot target with factor of 2
#plt.plot(x_target,bx_target_app,'--',color="black")
#plt.plot(x_target,by_target_app, color='orange')
#plt.plot(x_target,bz_target_app, color='orange')

#band showing theory approximation, most likely  between simulated fields
# for simulation
plt.fill_between(x_sim,bx_sim,bx_sim_app,facecolor='gray',alpha=0.12)
plt.fill_between(x_sim,by_sim,by_sim_app,facecolor='gray',alpha=0.12)
plt.fill_between(x_sim,bz_sim,bz_sim_app,facecolor='gray',alpha=0.12)

#COMSOL result

#plt.plot(pos_com,bx_com,color="magenta",label="$B_x(x,0,0)$")
#plt.plot(pos_com,by_com, color='orange',label="$B_y$")
#plt.plot(pos_com,bz_com, color='orange',label="$B_z$")

#plt.axhline(0, color='orange', linestyle='--')


plt.xlabel("Position along $x$-axis (m)",fontsize=14)
plt.ylabel("Coil $22$ Magnetic Field (nT)",fontsize=14)


ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]*3
handles=[ph[0]]+h[0:3]+[ph[1]]+h[3:6]+[ph[2]]+h[6:9]
#+[ph[4]]+h[12:15]
labels=[r'\underline{Measured}']+l[0:3]+[r"\underline{Simulated: In free space}"]+l[3:6]+[r"\underline{Image current effects: $\approx$ a factor of 2}"]+l[6:9]

#+[r"\underline{COMSOL}"]+l[12:15]


plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (m)")
plt.xlim([-1.1,1.1])
plt.ylim([-35,35])
plt.ylabel("Coil $22$ Magnetic Field (nT)")
plt.legend(handles, labels, ncol=3,fontsize=14)

plt.savefig("map_my_shims_coil22_models.png",dpi=300)

plt.show()


