'''
This code is an extension of the code used in Q1.py, instead of performing the
Uniform Random Walk search, this code performs Variable Neighbourhood Descent.
It outputs the result or prints "No assignment found".

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

###############Function for printing the output#########################
def result(model):
    print "s SATISFIABLE"
    print "v ",
    for i in range(len(model)):
        print "%d " % ((i + 1) * model[i]),
    print ""
########################################################################


def evaluate(cnf, model):
    # This function evaluates the score of a possible model assignment;
    # score is the number of unsatisfied clauses in the CNF. This function
    # take the CNF in matrix form and the model s as numpy array

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
    # This function generates atmost 10 random neighbours of the candidate
    # solution s by switching the value assignment of one variable. This
    # function take the CNF in matrix form and the model s as numpy array
    # and return a list of lists

    N = []  # Stores neighbours s' of s
    nVar = len(s)  # number of variables
    new = s
    for i in range(10):  # generating at most 10 new neighbours
        ran_num = random.randint(0, nVar - 1)
        new[ran_num] = -1 * new[ran_num]
        if not new in N:  # ignore already generated s'
            N.append(list(new))

    return N
##########################################################################


def VND(cnf, maxSteps):  # Variable Neighbourhood Descent
    length_v = len(cnf[0])
    s = np.ones(length_v)  # initial candidate solution array

    for x in range(length_v):
        s[x] = random.choice([1, -1])  # candidate solution
    score_s = evaluate(cnf, s)

    i = 1
    while(i < maxSteps):
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

##########################################################################
VND(CNF, 10000)  # Run the VND algorithm with 10000 maximum iterations

#stop = timeit.default_timer()

#print stop - start
