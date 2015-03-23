#!/usr/bin/env python
# coding: utf-8
import subprocess
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

#hostname = subprocess.call("hostname")
out, err = subprocess.Popen(["hostname"], stdout = subprocess.PIPE).communicate()
hostname = out.replace('\n', '')
print 'Hostname: %s' % hostname
out, err = subprocess.Popen(["free", "-m"], stdout = subprocess.PIPE).communicate()
memory = out.splitlines()
print 'Memory total: %s Memory used: %s' % show_memory(memory)
out, err = subprocess.Popen(["uptime"], stdout = subprocess.PIPE).communicate()
print 'Load average: %s %s %s' % load_average(out) 
out, err = subprocess.Popen(["df", "-h"], stdout = subprocess.PIPE).communicate()
#stdin, stdout, stderr = subprocess.call("df -h")
print 'Disk total: %s Disk used: %s Disk avail: %s' % show_df(out.splitlines())
