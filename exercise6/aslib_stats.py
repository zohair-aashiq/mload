
# coding: utf-8

# In[12]:

from argparse import ArgumentParser
import arff
import json
import numpy as np
from ast import literal_eval
import sys

parser = ArgumentParser()
parser.add_argument("-a", "--algoruns", dest="scenario",
                    default="SAT11-INDU", help="specify algorithm_runs.arff file")
args, unknown = parser.parse_known_args()

scenario = args.scenario

data = arff.load(open(str(scenario)))

stArray=np.array((data["data"]))
col_2=stArray[:,3]
col_21=col_2.astype(float)
algorithms = []
i=0
while(stArray[i,2].astype(str)) not in algorithms:
    algorithms.append(stArray[i,2].astype(str))   
    i+=1
f=0
h=len(algorithms)
num_ins=len(col_21)/h
final_values=np.zeros(h)
for y in range(num_ins):
    stArray2=[]
    for x in range(f,h):                                    
        stArray2=np.append(stArray2,col_21[x])
    final_values=np.vstack((final_values,stArray2,))
    f=f+len(algorithms)
    h=h+len(algorithms)
final_values=np.delete(final_values,0,0)
for b in range(len(final_values)):
    for c in range(len(final_values[0])):
        if final_values[b,c]==5000:
            final_values[b,c]=50000
oracle=[]
for z in range(num_ins):
    oracle=np.append(oracle,min(final_values[z]))
oracle=sum(oracle)/num_ins
print "Oracle:",oracle
single_best=[]

single_best=min(sum(final_values)/num_ins)
print "SB:",single_best
