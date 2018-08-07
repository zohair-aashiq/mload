
# coding: utf-8

# In[9]:

from subprocess import Popen, PIPE


# In[10]:

# Make a list of instances

files_list=[]
with open('train-e.txt','r') as train:
    for line in train:
        files_list.append(line.split('\n')[0])
with open('test-e.txt','r') as test:
    for line in test:
        files_list.append(line.split('\n')[0])


# In[15]:

# Compute features and save in a file features.csv
cmd='./features/features -base '+files_list[0]
io = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
(output, error) = io.communicate()

output = output.split('\n')

#header = 'instanceName,'+output[-3]+'\n'

with open('features.csv','w') as feats:
    feats.write(header)

    for i in files_list:
        cmd='./features/features -base '+i
        io = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
        (output, error) = io.communicate()
        output = output.split('\n')
        if error:
            break
        feats.write(i+','+output[-2]+'\n')


# In[ ]:



