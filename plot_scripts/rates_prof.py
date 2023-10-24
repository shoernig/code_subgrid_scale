import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({'font.size': 60}) 

#--------------------------------------------------------------------------------
weights = []
gwt = [line.rstrip('\n') for line in open('/home/b/b380620/plot_script/gwt.txt')]
for i in gwt:
    weights.append(float(i))

#-------------------------------------------------------

experiments = ['icon_aes_ctrl_cosp','icon_aes_ctrl_cosp_aggstoch']
names       = ['CTRL','AGGstoch']

#experiments = ['icon_aes_ctrl_cosp']
#names       = ['CTRL']
ipath = '/work/bb1093/b380620/icon-A_out/'
opath = '/work/bb1100/b380620/plots/mp_rates/'




labels = ['Frz','Dep','Mlt','Evp','Sed','Agg','Aci']
labels2 = ['Frz','Dep','Mlt','Evp','Sed','Agg','Aci','Total']
color_rate = ['black','red','orange','grey','deepskyblue','blue','limegreen']
markers    = ['.','p','v','s','*','h','^','D']

style = ['-','--']


st = 0
end = 200

plt.figure(figsize=(30,25))


def profile(var):
    avg = np.mean(var*1e6*3600,0)
    prof = np.average(np.mean(avg,axis=2),axis=1,weights=weights)
    return(prof)

def standard(var):
    standard = []
    per90    = []
    per10    = []
    for ilev in range(var.shape[1]):
        standard.append(np.std(var[:,ilev,:,:]))
        per10.append(np.percentile(var[:,ilev,:,:],10))
        per90.append(np.percentile(var[:,ilev,:,:],90))
    return(standard,per10,per90)
        
        

for exp,name in zip(experiments,names):
    ik = names.index(name)
    #ifile = ipath+exp+'/'+exp+'_1990.nc'
    ifile = ipath+exp+'/'+exp+'_2005-2009_avg.nc'
    print(ifile)
    nc = Dataset(ifile,'r')
    aci = nc.variables['acidiag'][:]
    agg = nc.variables['aggdiag'][:]
    sed = nc.variables['seddiag'][:]
    dep = nc.variables['depdiag'][:] 
    frz = nc.variables['frldiag'][:] 
    mlt = nc.variables['mltdiag'][:]
    evp = nc.variables['evpdiag'][:]
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    plev  = nc.variables['lev'][:]
    nc.close() 
    # if ik ==0:
    #     CTRL = agg
    # if ik ==1:
    #     AGG  = agg

    bars = [ frz, dep, -mlt, -evp, sed, -agg, -aci, ]
    #bars = [-agg,-aci,sed]
    lk = 0
    for ivar in bars:   
        avg_global = profile(ivar) 
        std,per10,per90 = standard(ivar)
        if (labels[lk] == 'Aci') & (ik==0):
            ctrl = avg_global
        if (labels[lk] == 'Aci') & (ik==1):
            agg  = avg_global
            for ilev in range(len(plev)):
                proc = (agg[ilev]-ctrl[ilev])/ctrl[ilev] * 100
                print(labels[lk],name,'  ',plev[ilev]/100,'   ',proc.round(2))
            
        
        
        #print(labels2[lk]+'('+name+')',avg_global.mean())
        #for ilev in range(len(plev)):
            #print(avg_global[ilev]-std[ilev],'   ',avg_global[ilev],'   ',avg_global[ilev]+std[ilev])
        plt.plot(avg_global,plev/100,linewidth=8.,
                 color=color_rate[lk],
                 linestyle=style[ik],
                 marker=markers[lk],
                 markersize=30.,
                 markerfacecolor="None",
                 markeredgewidth=7,
                 label=labels[lk]+' ('+name+')')
        #plt.fill_betweenx(plev/100,per10,per90,color=color_rate[lk],alpha=0.3)
        
        
        lk = lk+1


plt.ylim(100,1000)
plt.gca().invert_yaxis()
plt.grid(True)
plt.gca().set_xlabel('Process Rate [mg/kg hr$^{-1}$]')
plt.gca().set_ylabel('Pressure level [hPa]')
plt.legend(fontsize=60, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig('rates_prof.pdf',bbox_inches = "tight")
#plt.show()
plt.close()
