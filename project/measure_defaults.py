
# coding: utf-8

# In[1]:

import re
from subprocess import Popen, PIPE


# In[4]:

test_list=[]
with open('test-e.txt','r') as test:
    for line in test:
        test_list.append(line.split('\n')[0])

with open('test_defaults.csv','w') as f:
    f.write('InstanceID,SuccessPercentage,Steps_Mean\n') #File Header
    
    for inst in test_list:
        cmd='./saps/ubcsat -alg saps -runs 10 -timeout 10 -seed 441215575 -r satcomp -i '+inst
        cmd=cmd+' -alpha 1.189 -rho 0.5 -ps 0.1 -wp 0.03'
        
        io = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
        (output, error) = io.communicate()
        
        if error:
            break
        
        output_lines=output.split('\n')
        
        for line in range(len(output_lines)):
            if re.search('#', output_lines[line]):
                continue
                
            elif re.search('Variables',output_lines[line]):
                Percentage = output_lines[line+7].split(' ')[2]
                Steps_Mean = output_lines[line+8].split(' ')[2]
                break

        f.write(inst+','+Percentage+','+Steps_Mean+'\n')


# In[ ]:



