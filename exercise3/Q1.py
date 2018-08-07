'''
This program generates a matrix of order (n x m) to represent CNF, where n is the
number of Clauses in the CNF and m is the number of Variables in the CNF. Each
clause is represented by a row in the matrix. Each literal in the clause/row is
 represented by -1,0 or 1. For i representing the i-th variable, -1 represents a
negated variable(i) literal, 0 represents that variable(i) is absent in the clause
 and 1 represents a non-negated variable(i) literal.
A model assignment is represent by an array of size equal to number of Variables.
True variable assignment is represented by 1, and False by -1.
'''
import numpy as np
import sys
import re
import math
import random
from operator import itemgetter
import timeit

#start =  timeit.default_timer()

#s = open("factoring2.dimacs").read()
s = open(sys.argv[1]).read()

lines = s.split('\n')
length = len(lines)

#############Searching the file for p-line to get Stats#################
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
########################################################################

##############Generating a matrix to represent the CNF##################
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
########################################################################

#############Function to check the satisfiability of model##############
def check_URW(cnf, model):
    # array to store status of each clause, initially all 0 (false)
    length_c = len(cnf[:, 0])  # number of Clauses
    answer = np.zeros(length_c)

    for x in range(
            length_c):  # for all clauses/rows in CNF, check satisfiability
        y = np.multiply(cnf[x], model)
        # True if any literal of clause x is satisfied & stores 1 in answer[x]
        if 1 in y:
            answer[x] = 1

    if len(answer) == np.sum(answer):  # True if all clauses are satisfied
        return 1
    # print "not satisfied"
    return -1
########################################################################

###############Function for printing the output#########################
def result(model):
    print "s SATISFIABLE"
    print "v ",
    for i in range(len(model)):
        print "%d " % ((i + 1) * model[i]),
    print ""
########################################################################

#################Function for URW-for-SAT###############################


def URW(cnf, maxSteps):
    length_v = len(cnf[0])  # variables
    model = np.ones(length_v)
    for x in range(length_v):
        model[x] = random.choice([1, -1])

    steps = 0
    while (steps < maxSteps):
        if check_URW(cnf, model) == 1:
            result(model)
            return model
        # randomly select variable x in F
        ran_num = random.randint(0, length_v - 1)
        model[ran_num] = -1 * model[ran_num]
        steps += 1
    print "Uniform Random Walk: No assignment found."
    return None
########################################################################

URW(CNF, 10000)  # Calling Uniform Random Walk for 10000 steps

#stop = timeit.default_timer()

#print stop - start
