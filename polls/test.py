from django.shortcuts import render
import tarfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from fnmatch import fnmatch



from django.shortcuts import render
import tarfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings



#from unpack
import sys
file = sys.argv[-1] # get user input

import os
import glob

import os
from fnmatch import fnmatch
import tarfile



from pathlib import Path





@api_view(['POST','GET'])
def host_names(request):

    # filename = os.path.join(settings.FILES_DIR,'dc-esxi15.sacombank.corp.vn-vmsupport-2016-12-15@14-08-37')
    # file = os.listdir(filename)
    global os
    data = request.data
    filename = data['file_path']
    
    file = os.listdir(filename)
    root = filename
    pattern = "*.log"

    l =[]
    #loop getting all the *.log files
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                l.append(os.path.join(path, name))

    print(l)

    m = []
    #getting all the log files inside var/* which represtns host logs
    for i in l:
            if 'var' in i and 'log' in i :
                    m.append(i)
    s = []
    u = ['vmkernel.log','vkwarning.log','vmksummary.log','hostd.log','vpxa.log','shell.log','auth.log','syslog.log']
    for k in m:
        for n in u:
            if n in k:
                f = {'name':n,
                'path':k}
                s.append(f)
    

    
    # loop to read all vmfs/volumes/*/*.vmx
    pattern = "*.vmx"

    l =[]       # list variable
    t=[]        # list to store *.vmx required display name in dictrionary format
    vml = [] # varible to 
    #loop getting all the *.vmx files
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                l.append(os.path.join(path, name))
    nf = ''
    for k in l:
        x = file = open(k)
        for line in x:
            if('displayName' in line):
                nf = line
                break
        # t.append({
        #     'name':nf,
        #     'path':k
        # })
        t.append((os.path.dirname(k),nf))

    # print(t)

    # root = os.path.join+'dc-esxi15.sacombank.corp.vn-vmsupport-2016-12-15@14-08-37'
    pattern = "*.log"



    log =[]       # list variable
    # t=[]        # list to store *.vmx required display name in dictrionary format
    vml = [] # varible to 
    #loop getting all the *.vmx files
    # for path, subdirs, files in os.walk(root):
    #         for name in files:
    #                 if fnmatch(name, pattern):
    #                          log.append(os.path.join(path, name))
    mini_log=[]
    final_list=[]
    import glob, os
    for ldg in t:
            os.chdir(ldg[0])
            for file in glob.glob("*.log"):
                mini_log.append( {
                    'name':file,
                    'path':os.path.join(ldg[0],file)})
            final_list.append({
                    'name':str(ldg[1]).split()[2],
                    'path':os.path.join(ldg[0]),
                    'logs':mini_log,
            })
            mini_log=[]

    # print(final_list)

        


    return Response(data={
    'code':'200',
    'host':s,
    'vm': final_list
    })    
