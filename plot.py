import numpy as np
import matplotlib.pyplot as plt
import os
import pdb
import matplotlib
params = {
    'image.origin': 'lower',
    'image.interpolation': 'nearest',
    'image.cmap': 'gray',
    'axes.grid': False,
    'savefig.dpi': 1000,  # to adjust notebook inline plot size
    'axes.labelsize': 18, # fontsize for x and y labels (was 10)
    'axes.titlesize': 18,
    'font.size': 8, # was 10
    'legend.fontsize': 13, # was 10
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'figure.figsize': [5.47, 4.5],
    'font.family': 'serif',
}

matplotlib.rcParams.update(params)


sim_path = 'postProcessing/T_p_average/0.018/volFieldValue.dat'
data_vp = np.loadtxt(sim_path,comments='#',skiprows=2)
f=open(sim_path,"r")
lines=f.readlines()[4:]
time=[]
TAvg = []
pAvg = []
for x in lines:
    time.append(float(x.split('\t')[0]))
    TAvg.append(float(x.split('\t')[2]))
    pAvg.append(float(x.split('\t')[1]))
f.close()
pAvg = [i/101325 for i in pAvg]
fig, axs = plt.subplots(2,sharex=True)
axs[0].plot(time,pAvg,'k-',linewidth=2,label="Model")
axs[1].plot(time,TAvg,'k-',linewidth=2)


with open('cantera_results_noreac.txt') as f:
    file = f.readlines()[0:]
time_cnt=[]
p_cnt=[]
T_cnt=[]
rho_cnt = []
for i in file:
    data=i.strip().split('\n')
    time_cantera = [item.split(',')[0] for item in data if item]
    p_cantera = [item.split(',')[1] for item in data if item]
    T_cantera = [item.split(',')[2] for item in data if item]
    rho_cantera = [item.split(',')[3] for item in data if item]
    time_cnt.append((float(time_cantera[0])))
    p_cnt.append((float(p_cantera[0])))
    T_cnt.append((float(T_cantera[0])))
    rho_cnt.append((float(rho_cantera[0])))
time_cnt = [i-0.025 for i in time_cnt]
p_cnt = [i/101325 for i in p_cnt]

axs[0].plot(time_cnt,p_cnt,'ro',markevery=1000, markersize=7,label="Cantera")
axs[1].plot(time_cnt,T_cnt,'ro',markevery=1000, markersize=7)
axs[0].legend(loc=2,frameon=False)

axs[1].set_xlim([0.018,0.032])
axs[1].set_xticks([0.02,0.0225,0.025,0.0275,0.03])
axs[1].set_xticklabels(['-36','-18','0.0','18','36'])
axs[1].set_xlabel('Time [CAD]')

axs[0].set_ylim([10,60])
axs[0].set_yticks([10,35,60])
axs[0].set_yticklabels(['10','35','60'])
axs[0].set_ylabel('p [bar]')
axs[0].tick_params(direction='out',top=False,right=False)
axs[1].set_ylim([500,910])
axs[1].set_yticks([500,700,900])
axs[1].set_yticklabels(['500','700','900'])
axs[1].set_ylabel('T [K]')
axs[1].tick_params(direction='out',top=True,right=False)

plt.tight_layout()
plt.savefig('motoredP.png')

plt.show()


