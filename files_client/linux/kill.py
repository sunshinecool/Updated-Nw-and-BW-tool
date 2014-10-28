import subprocess

r = open('pid.txt')

t= r.readline()[:-1]

subprocess.call("kill -15 "+t,shell=True)
