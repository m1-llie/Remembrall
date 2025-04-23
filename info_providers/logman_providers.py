# record all the providers that are currently registered with the Win11 22H2 system
import subprocess


command = "logman query providers"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = process.communicate()

print(out.decode())
with open('logman_output.txt', 'w') as f:
    f.write(out.decode())
