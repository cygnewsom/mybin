#/bin/bash/python

import os
import subprocess
import sys

services = set()
my_services = []
failed = []
web_flag = False

def readServiceList():
    with open(os.path.join(os.path.expanduser('~'), "mybin/services.txt")) as f:
        file_txt = f.read()
        services_list = file_txt.split('\n')[:-1]
        for service in services_list:
            services.add(service)
        print services

def getServices():
    proc = subprocess.Popen(['git', 'diff', '--name-only', 'HEAD', 'HEAD^'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        print "git diff err\n"
        sys.exit(1)
    else:
        print "git diff successfully\n"
        lines = out.split()
        for line in lines:
            p = line.split('/')
            if (p[0] == 'common') or (p[0] == 'web'):
                web_flag = True
            elif p[0] in services:
                my_services.append(p[0])

        print my_services

def runLint(service, flag=False):
    stmt = ""
    if not flag:
        stmt = 'npm --prefix {} run lint -- --fix'.format(service)
    else:
        stmt = 'npm run lint -- --fix'
    print stmt
    proc = subprocess.Popen(stmt.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        print err
        failed.append("lint " + service)
    else:
        print out

def runFmt(service, flag=False):
    stmt = ""
    if not flag:
        stmt = 'npm --prefix {} run format:fix'.format(service)
    else:
        stmt = 'npm run format:fix'
    print stmt
    proc = subprocess.Popen(stmt.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        print err
        failed.append("format " + service)
    else:
        print out
    
def summary():
    if not failed:
        print "Lint & format run successfully\n"
    else:
        print "The following command failed:\n"
        for fail in failed:
            print fail

if __name__ == "__main__":
    path = os.getcwd()
    print(path)
    if (path != os.path.join(os.path.expanduser('~'), 'code')):
        print "not in the right dir\n"
        sys.exit(1)
    readServiceList()
    getServices()
    for service in my_services:
        runFmt(service)
        runLint(service)
    if web_flag:
        runFmt("", web_flag)
        runLint("", web_flag)
    summary()
