
# coding: utf-8

# In[16]:

from collections import Counter
from operator import add,sub
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
x_train=np.loadtxt("x_train.np")
y_train=np.loadtxt("y_train.np")
x_test=np.loadtxt("x_test.np")
y_test=np.loadtxt("y_test.np")

itrt1=[]
acc_sc1=[]
itrt2=[]
acc_sc2=[]
sigma1=[]
sigma2=[]
def configuration(crtrn,max_fturs,x_train,y_train,x_test):
    itrt=[]
    acc_sc0=[]
    sigma=[]
    for x in range(1,5):
        acc_sc=[]
        for y in range(1,2):
            clf = RandomForestClassifier(n_estimators=x,criterion=crtrn, max_features=max_fturs,warm_start=True)
            clf = clf.fit(x_train,y_train)
            y_prdct=clf.predict(x_train)
            a=accuracy_score(y_train,y_prdct)
            acc_sc.append(a)
        acc_sc0.append(np.mean(acc_sc))
        sigma.append(np.std(acc_sc))
        itrt.append(x)
        #print itrt  
    return acc_sc0,itrt,sigma
acc_sc1,itrt1,sigma1=configuration("gini","auto",x_train,y_train,x_test)
acc_sc2,itrt2,sigma2=configuration("entropy",None,x_train,y_train,x_test)
index=[i for i, j in enumerate(acc_sc1) if j >= 0.90]
print index[0]
print itrt1
print acc_sc1
itrt_limit=itrt1[index[0]]

#print itrt1
#print acc_sc2
#print itrt2
upper_limit1=[]
lower_limit1=[]
upper_limit2=[]
lower_limit2=[]
upper_limit1=map(add, acc_sc1, sigma1)
lower_limit1=map(sub, acc_sc1, sigma1)
upper_limit2=map(add, acc_sc2, sigma2)
lower_limit2=map(sub, acc_sc2, sigma2)
plt.plot(itrt1,acc_sc1)
plt.plot(itrt2,acc_sc2)
plt.fill_between(range(1, 5),upper_limit1,lower_limit1,
                    facecolor="yellow",
                    alpha=0.2)
plt.fill_between(range(1, 5),upper_limit2,lower_limit2,facecolor="blue",alpha=0.2)

print itrt_limit
plt.xlim(xmax=itrt_limit)
plt.ylim(ymax=0.90)

plt.show()


##########################part3############################
acc_sc1=[]
itrt1=[]
acc_sc2=[]
itrt2=[]
acc_sc1=[0.68091819699499179, 0.68191986644407354, 0.73507512520868123,
0.73465776293823037, 0.76181969949916517, 0.76420701168614358,
0.77575959933222038, 0.77792988313856437, 0.78993322203672789,
0.79210350584307165, 0.79948247078464096, 0.80202003338898153,
0.80686143572621016, 0.80577629382303828, 0.81013355592654424,
0.80868113522537566, 0.81308848080133567, 0.81247078464106837,
0.81823038397328873, 0.81570951585976625]
itrt1=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
acc_sc2=[0.70063439065108524, 0.70053422370617691, 0.75166944908180289,
0.75045075125208682, 0.77237061769616022, 0.77290484140233728,
0.78964941569282143, 0.78667779632721191, 0.79629382303839735,
0.79609348914858091, 0.80138564273789636, 0.80240400667779621,
0.80686143572621039, 0.80846410684474135, 0.81130217028380647,
0.81267111853088503, 0.81380634390651096, 0.81347245409015012,
0.81777963272120202, 0.81564273789649411]
itrt2=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
index=[i for i, j in enumerate(acc_sc1) if j >= 0.76]
print index[0]
print itrt1
print acc_sc1
itrt_limit=itrt1[index[0]]

print itrt_limit
plt.xlim(xmax=itrt_limit)
plt.ylim(ymax=acc_sc1[index[0]])
plt.plot(itrt1,acc_sc1)
plt.plot(itrt2,acc_sc2)
plt.show()



############################3Part3##################################################################################3

def exact_mc_perm_test(xs, ys, nmc):
   
    n, k = len(xs), 0
    diff = np.abs(np.mean(xs) - np.mean(ys))
    
    zs = np.concatenate([xs, ys])
   
    for j in range(nmc):
        np.random.shuffle(zs)
        k += 0.76 < np.abs(np.mean(zs[:n]) - np.mean(zs[n:]))
        print 
    return k / nmc
exact_mc_perm_test(itrt2, acc_sc2, 10000)


# In[ ]:



