
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold
import arff
import json
import numpy as np
from ast import literal_eval
import sys
data = arff.load(open("feature_values.arff"))
data_0 = arff.load(open("algorithm_runs.arff"))
data_1 = arff.load(open("cv.arff"))
features=json.dumps(data)
stArray=np.array((data["data"]))
stArray_1=np.array((data_1["data"]))
#print len(stArray[0])
features=stArray
features=features.astype(str)
cv=stArray_1
cv=cv.astype(str)
Matrix = [[0 for z in range(1)] for z in range(11)] 
for x in range(300):
    for y in range(300):
        if features[x,0]==cv[y,0]:
            Matrix[int(float(cv[y,2]))].append(features[x])
stArray=np.array((data_0["data"]))
col_21=stArray
algorithms = []
i=0
while(stArray[i,2].astype(str)) not in algorithms:
    algorithms.append(stArray[i,2].astype(str))   
    i+=1
f=0
h=len(algorithms)
num_ins=len(col_21)/h
final_values=np.zeros(90)
for y in range(num_ins):
    stArray2=[]
    for x in range(f,h):
        
        stArray2=np.append(stArray2,col_21[x])
    final_values=np.vstack((final_values,stArray2))
    
    f=f+len(algorithms)
    h=h+len(algorithms)
final_values=np.delete(final_values,0,0)
print len(final_values)
po=np.zeros(2)
for w in range(len(final_values)):
    d={}
    arr=[]
    for y in xrange(2,87,5):
        z=y+1
        d[final_values[w,y]]=[final_values[w,z]]
    e=min(d.items(), key=lambda x: x[1]) 
    arr.append(final_values[w,0])
    arr.append(e[0])
    po=np.vstack((po,arr))
Y = [[0 for z in range(1)] for z in range(11)] 
for x in range(300):
    for y in range(300):
        if po[x,0]==cv[y,0]:
            Y[int(float(cv[y,2]))].append(po[x])
print Matrix
"""clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(Matrix[], po)"""

import arff
import json
import numpy as np
from ast import literal_eval
import sys
data_1 = arff.load(open("cv.arff"))
stArray_1=np.array((data_1["data"]))
cv=stArray_1
cv=cv.astype(str)
data = arff.load(open("algorithm_runs.arff"))
#json.dumps(data)
#sys.argv[1]



