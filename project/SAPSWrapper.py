import sys, os, time, re
from subprocess import Popen, PIPE

# Read in first 5 arguments.
instance = sys.argv[1]
specifics = sys.argv[2]
cutoff =int(float(sys.argv[3]))
runlength = int(sys.argv[4])
seed = int(sys.argv[5])

# Read in parameter setting and build a dictionary mapping param_name to param_value.
params = sys.argv[6:]
configMap = dict((name, value) for name, value in zip(params[::2], params[1::2]))
 
# Construct the call string to SAPS.
cmd = "saps/ubcsat -alg saps -i %s -runs 10 -timeout %d -cutoff 100000 -r satcomp" %(instance,cutoff)
for name, value in configMap.items():
    cmd += " %s %s" %(name,  value)
    
# Execute the call and track its runtime.
io = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
(output, error) = io.communicate()

# Parsing of SAPS's output.
status = "CRASHED"
if (re.search('s UNKNOWN', output)):
    status = 'TIMEOUT'
if (re.search('s SATISFIABLE', output)) or (re.search('s UNSATISFIABLE', output)):
    status = 'SUCCESS'

output_lines=output.split('\n')

for line in range(len(output_lines)):
    if re.search('#',output_lines[line]):
	continue

    elif re.search('Variables', output_lines[line]):
	runlength = output_lines[line+8].split(' ')[2]    #STEPS_MEAN in Output
	runtime = output_lines[line+11].split(' ')[2]    #CPUTime_Mean in Output
	break
    
# Output result for SMAC.
print "Result for SMAC: %s, %s, %s, %s, 0" %( status, runtime, runlength, runlength)
