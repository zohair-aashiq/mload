
# coding: utf-8

# In[32]:

import os
import commands

train_list=[]
with open('train.txt','r') as train:
    for line in train:
        train_list.append(line.split('\n')[0])


# In[33]:

test_list=[]
with open('test.txt','r') as test:
    for line in test:
        test_list.append(line.split('\n')[0])


# In[41]:

#making lists of wrong files, and saving them later
new_train_list=[]
qcp_faults_train=[] #qcp
swgcp_faults_train=[] #swgcp

for i in xrange(len(train_list)):
    if(re.search('QCP', train_list[i])):
        with open(train_list[i],'r') as inst:
            for line in inst:
                if line.split('\n')[0].split(' ')[0] == "c":  # ignoring comments
                    continue
                else:
                    break
            Stats = line.split('\n')[0].split(' ')
            Variables = int(Stats[2])
            Clauses = int(Stats[3])
            if Variables == 0 or Clauses==0:
                qcp_faults_train.append(train_list[i])
            else:
                new_train_list.append(train_list[i])
    else:
        if (re.search('cnf', train_list[i])):
            new_train_list.append(train_list[i])
        else:
            swgcp_faults_train.append(train_list[i])


# In[42]:

#Same for test instances

new_test_list=[]
qcp_faults_test=[] #qcp
swgcp_faults_test=[] #swgcp

for i in xrange(len(test_list)):
    if(re.search('QCP', test_list[i])):
        with open(test_list[i],'r') as inst:
            for line in inst:
                if line.split('\n')[0].split(' ')[0] == "c":  # ignoring comments
                    continue
                else:
                    break
            Stats = line.split('\n')[0].split(' ')
            Variables = int(Stats[2])
            Clauses = int(Stats[3])
            if Variables == 0 or Clauses==0:
                qcp_faults_test.append(test_list[i])
            else:
                new_test_list.append(test_list[i])
    else:
        if (re.search('cnf', test_list[i])):
            new_test_list.append(test_list[i])
        else:
            swgcp_faults_test.append(test_list[i])


# In[54]:

qcp_faults_train.sort()
qcp_faults_test.sort()
swgcp_faults_train.sort()
swgcp_faults_test.sort()

with open('qcp_faults_train.txt','w') as qcp:
    for line in qcp_faults_train:
        qcp.write(line+"\n")
with open('qcp_faults_test.txt','w') as qcp:
    for line in qcp_faults_test:
        qcp.write(line+"\n")
        
with open('swgcp_faults_train.txt','w') as swgcp:
    for line in swgcp_faults_train:
        swgcp.write(line+"\n")
with open('swgcp_faults_test.txt','w') as swgcp:
    for line in swgcp_faults_test:
        swgcp.write(line+"\n")


# In[55]:

#train and test with no wrong files
with open('train-e.txt','w') as train_e:
    for line in new_train_list:
        train_e.write(line+"\n")
with open('test-e.txt','w') as test_e:
    for line in new_test_list:
        test_e.write(line+"\n")


# In[ ]:



