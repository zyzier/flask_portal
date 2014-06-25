#!/usr/bin/env python
# coding: utf-8

import paramiko 
from getpass import getpass
import re
import sys

# constant for color output
HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
ENDC = '\033[0m'


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
print HEADER + 'Hostname: %s' % hostname +ENDC

stdin, stdout, stderr = ssh.exec_command('free -m')
stdin, stdout, stderr = ssh.exec_command('free -m')
print GREEN + 'Memory total: %s Memory used: %s' % show_memory(stdout.read().splitlines()) + ENDC
    
stdin, stdout, stderr = ssh.exec_command('uptime')
print BLUE + 'Load average: %s %s %s' % load_average(stdout.read()) + ENDC 

stdin, stdout, stderr = ssh.exec_command('df -h')
print YELLOW + 'Disk total: %s Disk used: %s Disk avail: %s' % show_df(stdout.read().splitlines()) + ENDC

print '-------------------------------------------'

ssh.close()