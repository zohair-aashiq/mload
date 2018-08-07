import numpy as np
import sys
import re
import math
import random
import timeit
from operator import itemgetter
import matplotlib.pyplot as plt
import plot_scatter

def result(model):
    """
    Prints the model found
    
    This function is used to print the model assignment found by the SLS Algorithm.
    """
    print "s SATISFIABLE"
    print "v ",
    for i in range(len(model)):
        print "%d " % ((i + 1) * model[i]),
    print ""

def evaluate(cnf, model):
    """
    Evaluates the model assignment.
    
    This function evaluates the score of a possible model assignment;
    score is the number of unsatisfied clauses in the CNF. This function
    take the CNF in matrix form and the model s as numpy array
    """
    nClauses = len(cnf[:, 0])  # number of clauses
    # array to store status of each clause, initially all 0 (false)
    answer = np.zeros(nClauses)
    for x in range(nClauses):  # check satisfiability of each clause in the CNF
        y = np.multiply(cnf[x], model)
        # True if any literal of clause x is satisfied & stores 1 in answer[x]
        if 1 in y:
            answer[x] = 1

    count = 0  # for counting unsatisfied clauses
    for x in range(nClauses):
        if answer[x] == 0:
            count += 1
    return count


def randomize(s):
    """
    Finds the neighbours of the current candidate.
    
    This function generates atmost 10 random neighbours of the candidate
    solution s by switching the value assignment of one variable. This
    function take the CNF in matrix form and the model s as numpy array
    and return a list of lists
    """

    N = []  # Stores neighbours s' of s
    nVar = len(s)  # number of variables
    new = s
    for i in range(10):  # generating at most 10 new neighbours
        ran_num = random.randint(0, nVar - 1)
        new[ran_num] = -1 * new[ran_num]
        if not new in N:  # ignore already generated s'
            N.append(list(new))

    return N

def Tabu(cnf, maxSteps):
    """
    Perfoms Tabu Search, with size of Tabu List: 100
    
    This function performs the Tabu Search to find a possible solution for
    SAT satisfaction. The Tabu list stores the last 100 candid solutions.
    It prints the result if an assignment is found and returns
    it as a numpy array, or prints "No assignment found" and returns None
    
    The Search continues for maxSteps or 30 secs. This code is modified
    from third exercise to consider running time.    
    
    CNF = a matrix representation of the CNF
    maxSteps = Maximum Number of Iterations
    """
    start_time = timeit.default_timer() #to be used when considering running time
    
    length_v = len(cnf[0])
    s = np.ones(length_v)  # initial candidate solution
    sBest = []
    

    for x in range(length_v):
        s[x] = random.choice([1, -1])

    sBest.append(list(s))
    TabuList = []
    maxTabuSize = 100  # Tabu List stores 100 previous solution states
    steps = 0
    while(steps < maxSteps and (timeit.default_timer() - start_time) < 30):
        #while condition modified to consider runtime of 30 secs
        bestCandid = np.zeros(length_v)
        N = randomize(list(s))  # a list of lists containing neighbours of s
        score = [100] * len(N)
        for j in range(len(N)):
            score[j] = evaluate(cnf, np.array(N[j]))

        for i, sCandid in enumerate(N):
            if (not sCandid in TabuList) and score[
                    i] < evaluate(cnf, np.array(bestCandid)):
                bestCandid = sCandid

        s = bestCandid
        score_best = evaluate(cnf, np.array(bestCandid))
        if score_best < evaluate(cnf, np.array(sBest)):
            sBest = bestCandid

        if score_best == 0:
            result(np.array(bestCandid))
            return bestCandid

        TabuList.append(bestCandid)

        # if size of TabuList exceeded the limit, remove the first element
        if len(TabuList) > maxTabuSize:
            TabuList = TabuList[1:]

        steps += 1
    print "Tabu Search: No assignment found."
    return None

def VND(cnf, maxSteps):  # Variable Neighbourhood Descent
    """
    Performs Variable Neighbourhood Descent.
    
    VND: Generates a random candidate solution s, then generates atmost
    10 new neighbours of s and evaulates their scores. Finally, it prints
    the result if an assignment is found and returns it as a numpy array,
    or prints "No assignment found" and returns None output
    
    The Search continues for maxSteps or 30 secs. This code is modified
    from third exercise to consider running time.
    
    CNF = a matrix representation of the CNF
    maxSteps = Maximum Number of Iterations
    """
    
    start_time = timeit.default_timer() #to be used when considering running time
    length_v = len(cnf[0])
    s = np.ones(length_v)  # initial candidate solution array

    for x in range(length_v):
        s[x] = random.choice([1, -1])  # candidate solution
    score_s = evaluate(cnf, s)

    i = 1
    while(i < maxSteps and (timeit.default_timer() - start_time) < 30):
        #while condition modified to limit the running time
        N = randomize(list(s))  # a list of lists containing neighbours of s
        score = [1000] * len(N)

        for j in range(len(N)):
            score[j] = evaluate(cnf, np.array(N[j]))

        index = min(enumerate(score), key=itemgetter(1))[
            0]  # finding the index of min in score list

        s_best = np.array(N[j])

        if score[index] == 0:
            result(s_best)
            return s_best

        if score[index] < score_s:
            s = s_best
            score_s = score[index]
            i = 1
        else:
            i += 1
    print "Variable Neighbourhood Descent: No assignment found."
    return None

def read_file(n):
    """
    Function for reading the n-th input file from cnf_exercise5 directory.
    
    Read the input file and generates a matrix. This function generates a
    matrix of order (n x m) to represent CNF, where n is the number of
    Clauses in the CNF and m is the number of Variables in the CNF. Each
    clause is represented by a row in the matrix. Each literal in the
    clause/row is represented by -1,0 or 1. For i representing the i-th
    variable, -1 represents a negated variable(i) literal, 0 represents
    that variable(i) is absent in the clause  and 1 represents a 
    non-negated variable(i) literal.
    """
    #Reading the input file
    f1=("cnf_exercise5/random_ksat(",").dimacs")
    f2 = str(n).join(f1)
    
    #s= open("cnf_exercise5/random_ksat(8).dimacs").read()
    s=open(f2).read()
    #s = open(sys.argv[1]).read()

    lines = s.split('\n')
    length = len(lines)

    #Searching the file for p-line to get Stats#
    C = "c"
    for i in range(length):
        line = lines[i]
        if line[0] == C:  # ignoring comments
            continue
        else:
            p = i
            break

    Stats = lines[p].split(' ')
    Variables = int(Stats[2])
    Clauses = int(Stats[3])

    #Generating a matrix to represent the CNF
    CNF = np.zeros((Clauses, Variables))  # for CNF matrix

    i = p + 1  # the index of line after p-line
    j = 0  # for row number in CNF matrix
    while i < length - 1:
        if lines[i][0] == C:  # ignore any comments
            i += 1
            continue
        clause = lines[i].split(' ')

        for k in range(len(clause) - 1):
            x = int(clause[k])
            CNF[j][abs(x) - 1] = math.copysign(1, x)
        j += 1
        i += 1
    return CNF

#print RuntimeTabu
#print RuntimeVND

AvgRuntimeTabu=[]
AvgRuntimeVND=[]
for i in range(14):
    AvgRuntimeTabu.append(np.average(RuntimeTabu[i,:]))
    AvgRuntimeVND.append(np.average(RuntimeVND[i,:]))

#print AvgRuntimeTabu
#print AvgRuntimeVND

np.savetxt("Runtime_Tabu.txt",np.array(RuntimeTabu))
np.savetxt("Runtime_VND.txt",np.array(RuntimeVND))

#plotting Runtimes of both algorithms on instance#6
plt.plot(range(1,21),RuntimeTabu[5],'ro',label='Tabu')
plt.plot(range(1,21),RuntimeVND[5],'bo',label='VND')
plt.xlabel('Iteration')
plt.xlim(1,20)
plt.ylabel('Runtime (s)')
plt.ylim(0,40)
plt.title('Runtimes Comparison of Tabu Search and VND')
plt.legend()
plt.show()

#Generating Scatter Plot
#help(plot_scatter.plot_scatter_plot)
plot_scatter.plot_scatter_plot(np.array(AvgRuntimeTabu), np.array(AvgRuntimeVND),labels=["Tabu","VND"], title='Tabu VS VND',save='scatter.png')
plt.show()

#Generating Boxplot
#help(plt.boxplot)
plt.figure()
plt.boxplot((RuntimeTabu,RuntimeVND))
plt.show()
