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
bx_sim=bx_sim*1e9 # convert to nT
by_sim=by_sim*1e9
bz_sim=bz_sim*1e9
#print('sim data is:',data)
#print(bx_sim)

#target field data
data=np.transpose(np.loadtxt('xscan_onesheet_target.out'))
x_target,bx_target,by_target,bz_target=data
bx_target=bx_target*1e9 # convert to nT
by_target=by_target*1e9
bz_target=bz_target*1e9
print('target data is',data)
print(bx_target)
print('by data here::::')
print(by_target)
print('z data hereeee::::')
print(bz_target)

# load metadata about the theoretical fields
import json
with open('data.json') as json_file:
    graphdata=json.load(json_file)
    
#measurement fileds    
    
#open data file name (obtained from TRIUMF) with field  measurements
data_file_name=np.transpose(np.loadtxt('xscan_onesheet_target.out')) #chnage xscan.out with actual meauremnt obtained from TRIUMF!
print(data_file_name)
# turn on the coil
# make a measurement of the magnetic field
x_data=[]
y_data=[]
z_data=[]

#position [x,y,] position
for i in range(3):
    position=i 

    voltages_on =data_file_name[1]  #field measure
    nT_on = data_file_name[2]  #offset_value

    # turn neg the coil
    # make a measurement of the magnetic field
    
    voltages_off= data_file_name[0]
    nT_off=  data_file_name[1]
    
    #diffrential magnetic field
    
    voltages_delta=[voltages_on[i]-voltages_off[i] for i in range(len(voltages_on))]
    nT_delta=[(nT_on[i]-nT_off[i])/2 for i in range(len(voltages_on))] # divide by two because subtracting neg from pos
   


    x_data.append(nT_delta[0])
    y_data.append(nT_delta[1])
    z_data.append(nT_delta[2])
    # Print out the measurement and the current position
    print(f"Position: {position}, Magnetic Field Measurements (X, Y, Z): {nT_delta}")
    
    with open(data_file_name, "a") as data_file:  # Open the file in append mode
        data_file.write(f"{position[0]} {position[1]} {position[2]} {nT_delta[0]} {nT_delta[1]} {nT_delta[2]}\n")

#current off

# used to test graphing
#x_data=range(len(positions))
#y_data=range(len(positions))
#z_data=range(len(positions))
x_data=np.array(x_data)
y_data=np.array(y_data)
z_data=np.array(z_data)


# fix measurement axes to be as in simulation

# position:
# The scan direction is the minus x direction in simulation

# fluxgate measurement:

# The fluxgate z-axis is aligned with the minus x direction in simulation.

# The fluxgate y-axis is aligned with the minus z direction in simulation.

# According to the right-hand rule, the fluxgate x-axis is aligned
# with the plus y direction in simulation.

plt.figure()
plt.scatter(-positions[:,0]*.01,-z_data,color="b",label="$B_x(x,0,0)$ meas",marker='.')
plt.scatter(-positions[:,0]*.01,-x_data,color="r",label="$B_y(x,0,0)$ meas",marker='.')
plt.scatter(-positions[:,0]*.01,y_data,color="g",label="$B_z(x,0,0)$ meas",marker='.')

# now plot simulation on top of this
plt.plot(x_sim,bx_sim,color="b",label="$B_x(x,0,0)$ sim")
plt.plot(x_sim,by_sim,color="r",label="$B_y(x,0,0)$ sim")
plt.plot(x_sim,bz_sim,color="g",label="$B_z(x,0,0)$ sim")


plt.plot(x_target,bx_target,'--',color="b",label="$B_x(x,0,0)=%s$"%(graphdata['Pix']))
plt.plot(x_target,by_target,'--',color="r",label="$B_y(x,0,0)=%s$"%(graphdata['Piy']))
plt.plot(x_target,bz_target,'--',color="g",label="$B_z(x,0,0)=%s$"%(graphdata['Piz']))

plt.xlabel("Position along $x$-axis (cm)")
plt.ylabel("Magnetic Field (nT)")



ax=plt.gca()
h,l=ax.get_legend_handles_labels()
ph=[plt.plot([],marker="", ls="")[0]]*3
#handles=[ph[0]]+h[::3]+[ph[1]]+h[1::3]+[ph[2]]+h[2::3]
#labels=["Title 1:"]+l[::3]+["Title 2:"]+l[1::3]+["Title 3:"]+l[2::3]
handles=[ph[0]]+h[0:3]+[ph[1]]+h[3:6]+[ph[2]]+h[6:9]
labels=[r'\underline{Measured}']+l[0:3]+[r"\underline{Simulated}"]+l[3:6]+[r"\underline{Target} $(\ell,m)=(%d,%d)$"%(graphdata['l'],graphdata['m'])]+l[6:9]

plt.rc('text',usetex=True)
plt.xlabel("Position along $x$-axis (cm)")
plt.ylabel("Magnetic Field (nT)")
plt.legend(handles, labels, ncol=3)


plt.savefig("field_measurements_%d_%d.png"%(graphdata['l'],graphdata['m']),dpi=300,bbox_inches='tight')

plt.show()

