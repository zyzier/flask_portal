#!/usr/bin/env python
# coding: utf-8

import paramiko 
from getpass import getpass
import re
import sys

def show_memory(raw_result):
    for string in raw_result:
        if re.search(r'Mem:', string):
            result = string.split()
            break
    return (result[1] , int(result[2]) - int(result[6]))

def load_average(raw_result):
    result = raw_result.split()
    return (result[-3], result[-2], result[-1])

def show_df(raw_result):
    for string in raw_result:
        if re.search(r'/', string):
            result = string.split()
            break
    return (result[1] , result[2], result[3])

user = 'peps'
#password = getpass()
#If password set from command line, like eval ... etc, then it will be executed
#If not, it will draw the promt in commandline on server
if sys.stdin.isatty():
    print 'Using term'
    password = getpass()
else:
    print 'Using readline'
    password = sys.stdin.readline().rstrip()


server = '46.246.111.126'
port = 2525
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


ssh.connect(server, username = user, password = password, port = port)
stdin, stdout, stderr = ssh.exec_command('hostname')
hostname = stdout.read().replace('\n', '')
print 'Hostname: %s' % hostname
stdin, stdout, stderr = ssh.exec_command('free -m')
stdin, stdout, stderr = ssh.exec_command('free -m')
print 'Memory total: %s Memory used: %s' % show_memory(stdout.read().splitlines())  
stdin, stdout, stderr = ssh.exec_command('uptime')
print 'Load average: %s %s %s' % load_average(stdout.read()) 
stdin, stdout, stderr = ssh.exec_command('df -h')
print 'Disk total: %s Disk used: %s Disk avail: %s' % show_df(stdout.read().splitlines())
ssh.close()
