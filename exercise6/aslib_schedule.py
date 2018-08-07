
# coding: utf-8

# In[665]:

import arff
import json
import numpy as np
import sys
import random
from operator import itemgetter
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-a", "--algoruns", dest="scenario",
                    default="SAT11-INDU", help="specify algorithm_runs.arff file")
args, unknown = parser.parse_known_args()
scenario = args.scenario

data = arff.load(open(str(scenario)))


stArray=np.array((data["data"]))

algorithms = []
i=0
while(stArray[i,2].astype(str)) not in algorithms:
    algorithms.append(stArray[i,2].astype(str))
    i+=1

#global variables
n_algos = len(algorithms)
runtimes = stArray[:,3].astype(float)
n_insts = len(runtimes)
runtimes = np.reshape(runtimes,(n_insts/n_algos,n_algos))
cutoff = 5000
max_possible_score = 100000
min_time_slice = 10
max_time_slice = 1000
step_time_slice = 10
iterations = 10    #for repeated search
max_steps_SLS = 60


# In[666]:

def algo_schedule(permutation, assignment):
    """
    Computes the average runtime and timeouts of the
    Algorithm Schedule.
    
    Attributes: - Permutation of algorithms
            - Time slice assignment for the algorithm
    Returns: - Average Runtime
             - number of Timeouts
    """
    permutation = np.array(permutation)
    assignment = np.array(assignment)

    schedule_time = np.zeros(n_insts/n_algos)
    
    for i in xrange(len(schedule_time)):    #for every instance
        schedule_flags = np.zeros(n_insts/n_algos)    #to check if the instance is solved or timeouts
        while(schedule_flags[i] == 0):
            for k in permutation:    #for all elements of permutation (all algos)
                if runtimes[i,k] <= assignment[k]:
                    schedule_time[i] += runtimes[i,k]
                    schedule_flags[i] = 1    #indicates solved
                    #break
                else:
                    schedule_time[i] += assignment[k]
                    if schedule_time[i] >= cutoff:
                        schedule_time[i] = 10 * cutoff
                        schedule_flags[i] = -1    #indicates timeout
                        #break
    
    #schedule_time = np.clip(schedule_time,min_time_slice, cutoff)
    
    timeouts = 0
    for i,j in enumerate(schedule_time):
        if j==10*cutoff:
            #schedule_time[i]=10*cutoff    #PAR10
            timeouts+=1
    avg_time = np.average(schedule_time)
    
    return avg_time, timeouts


# In[670]:

def VND_assignment(permutation, maxSteps):     #Variable Neighbourhood Descent
    """    
    Performs Variable Neighbourhood Descent to find
    time assignment for the algorithms. It uses
    algo_schedule() to compare scores. In each iteration,
    the VND generates atmost 10 neighbouring candid
    solutions and compares the scores. Finally, it 
    returns the time assignment with the best score.
    
    Attributes: Permutation: permutation of algorithm,
                used to compute score of the assignment
                maxSteps: max SLS steps to be performed
    Returns: - (array) best algorithm time slice assignment found
    """
    permutation = np.array(permutation)
    
    s = np.ones(n_algos)    #initial candidate solution array
    
    randomchoice = range(min_time_slice, max_time_slice, step_time_slice)
    i=0    
    while(i < n_algos):
        s[i] = random.choice(randomchoice)
        if np.sum(s) > cutoff: 
            s = np.ones(n_algos)
            i=-1
        i+=1
    
    avg_score_s, timeout_score_s = algo_schedule(permutation, s)

    i = 1
    while(i < maxSteps):
        N = randomize_assignment(list(s))    #a list of lists containing atmost 10 neighbours of s
        score = [max_possible_score] * len(N)
        
        for j in range(len(N)):
            x,score[j] = algo_schedule(permutation, np.array(N[j]))
        
        index = min(enumerate(score), key=itemgetter(1))[0]    #finding the index of min in score list
        
        s_best = np.array(N[index])
        
        if score[index] == 0:
            return s_best
        
        if score[index] < timeout_score_s:
            s = s_best
            timeout_score_s = score[index]
            i = 1
        else:
            i += 1
        #i += 1
    #print "Variable Neighbourhood Descent: No assignment found."
    return s_best


# In[671]:

def randomize_assignment(s):
    """
    Used by VND_assignment()
    
    Attributes: s: candidate solution of SLS aglorithm
    Returns: a list of atmost 10 random neighbours of the candidate solution s.
    """
        
    N = []    #Stores neighbours s' of s
    nVar = len(s)    #number of variables
    new = s
    for i in range(10):    #generating at most 10 new neighbours
        ran_idx = random.randint(0, nVar -1)
        #ran_idx2 = random.randint(0, nVar -1)
        ran_num = random.randint(min_time_slice+1, max_time_slice)
        add_or_sub = random.choice([1,-1])
        new[ran_idx] = new[ran_idx] + add_or_sub * ran_num
        #new[ran_idx2] = new[ran_idx] + -1 * add_or_sub * ran_num    #to ensure time assignment sum < cutoff
        new[ran_idx] = np.clip(new[ran_idx], min_time_slice, cutoff)
        if not new in N or np.sum(new) <= cutoff:    #ignore already generated s' or if s.sum is above cutoff
            N.append(list(new))
            
    return N


# In[673]:

def VND_permutation(assignment, maxSteps):     #Variable Neighbourhood Descent
    """
    Performs Variable Neighbourhood Descent to find
    permutation of the algorithms. Uses algo_schedule() 
    to compare scores of different permuations.
    
    Attributes: - assignment: time slice assignment for algorithms,
                used to compute score of the permutation
                - maxSteps: max SLS steps to be performed
    Returns: - (array) best permutation of algorithms found
    """
    
    assignment = np.array(assignment)
    
    s = np.random.permutation(n_algos)    #initial candidate solution array
    
    """i=0    
    while(i < n_algos):
        s[i] = random.choice(randomchoice)
        if np.sum(s) > cutoff: i=0
        i+=1"""
    avg_score_s, timeout_score_s = algo_schedule(s, assignment)

    i = 1
    while(i < maxSteps):
        N = randomize_permutation(list(s))    #a list of lists containing atmost 10 neighbours of s
        score = [max_possible_score] * len(N)
        
        for j in range(len(N)):
            x,score[j] = algo_schedule(np.array(N[j]), assignment)
        
        index = min(enumerate(score), key=itemgetter(1))[0]    #finding the index of min in score list
        
        s_best = np.array(N[index])
        
        if score[index] == 0:
            return s_best
        
        if score[index] < timeout_score_s:
            s = s_best
            timeout_score_s = score[index]
            i = 1
        else:
            i += 1
    #print "Variable Neighbourhood Descent: No assignment found."
    return s_best


# In[674]:

def randomize_permutation(s):
    """
    Used by VND_permutation()
    
    Attributes: s: candidate solution of SLS algorithm
    Returns: a list of atmost 10 random neighbours of the candidate solution s.
    """
        
    N = []    #Stores neighbours s' of s
    nVar = len(s)    #number of variables
    new = s
    for i in range(10):    #generating at most 10 new neighbours
        ran_num_1 = random.randint(0, nVar - 1)
        ran_num_2 = random.randint(0, nVar - 1)
        new[ran_num_1], new[ran_num_2] = new[ran_num_2], new[ran_num_1]
        if not new in N:    #ignore already generated s'
            N.append(list(new))
            
    return N



# In[ ]:

##########################################################################################
perm = range(n_algos) #initial permutation, guess!
assigns_list=[]
permuts_list=[]
timeouts_list=[]
#runtimes_list=[]
for i in range(iterations):
    assgn = VND_assignment(perm, max_steps_SLS)
    perm = VND_permutation(assgn, max_steps_SLS)
    r,t = algo_schedule(perm, assgn)
    assigns_list.append(assgn)
    permuts_list.append(perm)
    timeouts_list.append(t)
    #runtimes_list.append(r)
    #print "%d: avg: %f timeouts: %d"%(i,r,t)


# In[ ]:

index = min(enumerate(timeouts_list), key=itemgetter(1))[0]
permutation_final = permuts_list[index]
assignment_final = assigns_list[index]
print "Avg Runtime: %f, Timeouts: %d"%(algo_schedule(permutation_final, assignment_final))


# In[ ]:

assignment_display = dict(zip(algorithms, assignment_final))
permutation_display = []
for i in range(n_algos):
    permutation_display.append(algorithms[permutation_final[i]])


# In[ ]:

print "Assignment: ",assignment_display


# In[ ]:

print ""
print "Permutation: ",permutation_display


# In[ ]:



