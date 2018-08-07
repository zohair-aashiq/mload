'''imported the csp file and then partition the data into 2 parts.
one is  domain and other is constraints.
Convereted the variabes and of their domains into a dictionary and 
assinged each variable its domain.Then further partition the constraints 
on the bases of arthamtics operatores "+","-","*","/","%" and made the 
dictionaries of each constraints on basis of arthematic operators. 
Took randomaly one value from each domaina & check whether it satisfies
 the constraints or not until all constraints are satsifies. ''' 

import pandas as pd
import numpy as np
import sys
import random
import json
import re
from itertools import izip
import itertools
import pprint
with open(sys.argv[1]) as fp:
	csp = json.load(fp)
	matrix_1=np.matrix(csp)
	col_num=np.array(matrix_1.shape)
	i=col_num[1]
	domain=[]
	cons_1=[]
	c='int'
	for x in range(0,i):	
		matrix_2=matrix_1[:,x]
		matrix_3=np.array(matrix_2)
		merged_list = list(itertools.chain(*matrix_3))
		merged_list1 = list(itertools.chain(*merged_list))
		if merged_list1[0]==c:                        #partition of data into domain part 
			domain.append(merged_list1)
		elif merged_list1[0]=='alldifferent':	      #partition of data into alldiffernt part 
			cons_1.append(merged_list1)
	#i2=len(domain)
	domain_dm=np.array(domain)
	domain_dimension=np.array(domain_dm.shape)
	row_no=domain_dimension[0]
	col_no=domain_dimension[1]
	variable=[]
	start_rng=[]
	end_rng=[]
	variables=[]
	dictionary={}
	pk=[]
	for x2 in range(0,row_no):
		vari=domain_dm[x2,1]	
		rng1=domain_dm[x2,2]
		rng2=domain_dm[x2,3]		
		rng1=int(rng1)
		rng2=int(rng2)
		vari2=str(vari)
		start_rng.append(rng1)
		end_rng.append(rng2)
		variables.append(vari2)
		#print start_rng		
		#print end_rng
		#print variables
		rng2=rng2+1
		for x in range(rng1,rng2):
    			dictionary.setdefault(vari2, []).append(x)           #assign domain to each variable in form of dictionary 
	i=len(cons_1)
	cons={}
	#random=[]
	q_val1=random.choice(dictionary['q_1'])
	q_val2=random.choice(dictionary['q_2'])
	q_val3=random.choice(dictionary['q_3'])
	q_val4=random.choice(dictionary['q_4'])
	q_v={}
	#print q_val2
	#print q_val3
	#print q_val4
	q=[]
	val=[]
	z=[]
	q1=[]
	val1=[]
	z1=[]
	q2=[]
	val2=[]
	z2=[]
	q3=[]
	val3=[]
	z3=[]
	q4=[]
	val4=[]
	z4=[]
	q5=[]
	val5=[]
	z5=[]
	for x3 in range(0,i):	
	#pk=np.array(cons_1[0])
		pk=cons_1[x3]
		i2=len(pk)
		#print i2
		for x in range(0,i2):
			pk2=pk[x]
			i3=len(pk2)
			#print pk
			#print pk2
			#print i3
			if (pk2[0]=='+'):
				#for x2 in range(1,i3):
					#cons["string{0}".format(x2)]=pk2[x2]
				q.append(pk2[1])
				val.append(pk2[2])
				z=dict(zip(q, val))
				#print z
					#print cons
					#print cons['string1']
				val	#print cons['string2']
			elif (pk2[0]=="-"):
				q1.append(pk2[1])
				val1.append(pk2[2])
				z1=dict(zip(q, val))
				#print z1
			elif (pk2[0]=="*"):
				q2.append(pk2[1])
				val2.append(pk2[2])
				z2=dict(zip(q, val))
			elif (pk2[0]=='/'):
				q3.append(pk2[1])
				val3.append(pk2[2])
				z3=dict(zip(q, val))
			elif (pk2[0]=='%'):
				q4.append(pk2[1])
				val4.append(pk2[2])
				z4=dict(zip(q, val))
			else:
				q5.append(pk2[1])
				val5.append(pk2[2])
				z5=dict(zip(q, val))
	print z1
	print z2
	print z3
	print z4
###we Can't complete the task because of first two tasks took lots of time and we don't have much time for this task.

