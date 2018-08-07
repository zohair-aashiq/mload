
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:

def report(steps):
    """
    Returns no. of timeouts, PAR1 & PAR10 for a given array
    """
    
    timeouts = 0 #count
    par10 = 0
    L = len(steps)
    par1 = steps.sum()
    
    for i in steps:
        if i == 100000:
            timeouts+=1
            par10 += 1000000
            continue
        par10 += i
    
    return timeouts, par1/L, par10/L


# In[3]:

#Measuring defaults on test instances with pcs-file's default parameter settings
score_pcs_def = pd.read_csv("test_defaults.csv")
score_pcs_def = score_pcs_def["Steps_Mean"].values
print 'Default(pcs-file) #TIMEOUT, PAR1, PAR10:'
print report(score_pcs_def)


# In[4]:

#Measuring performance with algorithm's default parameters
score_algo_def = pd.read_csv("test_defaults_algodefaults.csv")
score_algo_def = score_algo_def["Steps_Mean"].values
print 'Default(algorithm) #TIMEOUT, PAR1, PAR10:'
print report(score_algo_def)


# In[5]:

#Measuring performance with configured parameters; SMAC wall-time 24 hours
score24n = pd.read_csv("Output24hr/new_validation/validationObjectiveMatrix-detailed-traj-run-229549472-walltime.csv")
score24n = score24n['Objective of validation config #1'].values
print 'Configured #TIMEOUT, PAR1, PAR10:'
print report(score24n)


# In[10]:

#Plotting histogram (RTD)

plt.figure()

X = [score24n,score_pcs_def, score_algo_def]    #Configured runlengths; Default runlengths

plt.hist(x=X, bins=len(score24n), normed=True,cumulative=True,         histtype='step', color=['r','b','g'], label=['Configured','pcs-Default','Algo-Default'])

plt.xlabel('Runlength (log-scale)')
plt.xscale('log')
plt.xlim([300,100000])
plt.ylabel('P(solve)')
plt.title('Performance on Test Instances')
plt.grid(True, which='both')
plt.legend(loc='upper left', fontsize='medium')
#plt.show()
plt.savefig("RTD_trunc")


# In[8]:

#Plotting Boxplot
plt.figure()
plt.boxplot(x=[np.transpose(score_pcs_def), np.transpose(score24n)],labels=['Default', 'Configured'])
plt.grid(True, which='major')
plt.ylabel('Runlength')
plt.title('Boxplots for RTD on Test Instances')
plt.savefig("Boxplot")


# In[12]:

#Plotting Boxplot with Runlength Ratio
plt.figure()
plt.boxplot(x=(np.transpose(score_pcs_def)/np.transpose(score24n)))
plt.xlabel('Default/Configured')
plt.grid(True, which='major')
plt.ylim([0,5])
plt.ylabel('Runlength Ratio')
plt.title('Boxplot with Runlength Ratio')
plt.savefig('Boxplot_ratio_trunc')


# In[16]:

# For Scatter Plot
plt.figure()
line=np.array(range(0,100000,100))    #for diagonal line
plt.scatter(x=score_pcs_def[0:5028],y=score24n[0:5028],marker='+',c='r',label='SWGCP')    #red for SWGCP instances
plt.scatter(x=score_pcs_def[5028:],y=score24n[5028:],marker='+',c='b',label='QCP')    #blue for QCP instances
plt.scatter(x=line, y=line, s=0.1)
plt.legend(loc='upper left', fontsize='medium')
plt.xlim([0,100000])
plt.ylim([0,100000])
plt.xlabel('Default')
plt.ylabel('Configured')
plt.title('Scatter Plot Config. vs Default')
plt.savefig('Scatter')


# In[ ]:



