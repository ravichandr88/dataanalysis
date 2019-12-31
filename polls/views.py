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



@api_view(['POST'])
def extract(request):
    my_file = Path(request.data['file_path'])
    

    if my_file.is_file():

        fn = my_file
        print(my_file)
        try:
            print(fn, tarfile.is_tarfile(fn))
        except (IOError, err):
                print(fn, err)

        
        dir_path = os.path.dirname(my_file)

        t = tarfile.open(fn, 'r')
        #check if the tar file is already extracted or not
        
        
        fldr_name =  t.getnames()[0]
        # check whether the name has a suffix 'README'
        if '/' in str(fldr_name):
           fldr_name = str(fldr_name).split('/')[0]
        file_path = os.path.join(dir_path,fldr_name)


        if os.path.exists(file_path):
            print('already exists')
            return Response(data={
            'code':'200',
            'path':file_path,
            'name':fldr_name
        })
        #find the folder name
        #.ZIP, .RAR, .ARJ, .TAR.GZ, and .TGZ

        #extract the tar file
        t.extractall(path=dir_path)

        return Response(data={
            'code':'200',
            'path':file_path,
            'name':fldr_name
        })

    else:
            return Response(data={
                'code':'400',
                'message':'File does not exists'
            })


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
    print(m)
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

# funtion to support file browser
@api_view(['POST'])
def index(request):
    drty_lst=[]
    data = request.data
    filepath = data.get('filepath')
    #check whetehr given path is a file or folder
    if os.path.isfile(filepath):
        filedata = open(filepath,'r')
        fl = []
        for i in filedata.readlines():
            fl.append(i)
        return Response(data={
            'code':'200',
            'type':'file',
            'body':fl
        })


    else:
        if(filepath == '' or filepath == request.data['file_path']):             # empty means the starting page
            drty = request.data['file_path']
        else:
            # drty = os.path.join(settings.FILES_DIR,filepath)
            drty = filepath

        drty_lst = []
        jukn = os.listdir(drty)
        for i in jukn:
            drty_lst.append({
            'dir_nme':i,
            'dir_path':os.path.join(drty,i)
        })
        
        return Response(data={
            'code':'200',
            'body':drty_lst,
            'type':'dir'
            })

# qry_rslt = []

import datetime

@api_view(['POST'])
def analysis(request):
    data = request.data

    #An interface which holds the file name and lines queried from the file.
    qry_data = {'file_name':'',
                'file_data':[]
                }
    qry_rslt = []
    for i in data:
        
        for j in i.get('list'):
            #add the file name to the interface dictionay
            qry_data['file_name'] = j
            if '.log' in j:     #checking whethe rthe item is a file 
                fle = open(j,'r')
                for fle_lns in fle.readlines():
                    str_tme = i.get('timi')
                    if str(str_tme) != '':      # check whether the line is within the time given
                        fle_tme = str(fle_lns[:10])
                        fle_tme_l = fle_tme.split('-') 
                        str_tme_l = str(str_tme).split('-')
                        str_tme = ''
                        fle_tme = ''
                        for mk in range(0,3):
                            str_tme = str_tme_l[mk] + str_tme
                            fle_tme = fle_tme_l[mk] + fle_tme
                        tme = datetime.datetime.strptime(fle_tme, '%d%m%Y').date()
                        qry_tme = datetime.datetime.strptime(str_tme, '%d%m%Y').date()
                        if tme >= qry_tme:
                            qry_data['file_data'].append(fle_lns)
                    elif i.get('string') in fle_lns:
                        qry_data['file_data'].append(fle_lns)
                qry_rslt.append(qry_data.copy())    
            else:
                os.chdir(j) 
                for fle in glob.glob("*.log"):      #start iterating all *.log files
                    
                    #Add file anme to the dictionary
                    
                    qry_data = {
                            'file_name':fle,
                            'file_data':[]
                            }
                    fle_jk = os.path.join(j,fle)
                    flen = open(fle_jk,'r')
                    for fle_lns in flen.readlines():
                        str_tme = i.get('timi')
                        if str(str_tme) != '':      # check whether the line is within the time given
                            fle_tme = str(fle_lns[:10])
                            fle_tme_l = fle_tme.split('-')
                            str_tme_l = str_tme.split('-')
                            str_tme = ''
                            fle_tme = ''
                            for mk in range(0,3):
                                str_tme = str_tme_l[mk] + str_tme
                                fle_tme = fle_tme_l[mk] + fle_tme
                            tme = datetime.datetime.strptime(fle_tme, '%d%m%Y').date()
                            qry_tme = datetime.datetime.strptime(str_tme, '%d%m%Y').date()
                            if tme >= qry_tme:
                                qry_data['file_data'].append(fle_lns)
                        elif i.get('string') in fle_lns:
                            qry_data['file_data'].append(fle_lns)
                        # if i.get('string') in fle_lns:
                    qry_rslt.append(qry_data.copy())
                    qry_data = {
                'file_name':'',
                'file_data':[]
                }
        # tmp_qry_rslt = qry_data.copy()
        # qry_rslt.append(tmp_qry_rslt)
        #refreshing the data object for every directory or file
        qry_data = {
                'file_name':'',
                'file_data':[]
                }
    return Response(data={
        'code':'200',
        # 'str_tme':tme,
        # 'fle_tme':qry_tme,
        # 'body':[]
        'body':qry_rslt
    })



@api_view(['POST'])
def host_dtls(request):
    # root =   os.path.join(settings.FILES_DIR,'esx-dc-esxi15.sacombank.corp.vn-2016-12-15--07.08')
    root = request.data['file_path']
    pattern = '*.txt'


    #details of host division is stored in 'hostDetails'


    data_store_info = ''
    data_lcl_vmfs = ''
    nicinfo_fle = ''
    core_adaptr_fle = ''
    pattern = '*.txt'

    hostdtl =''     #to store the host list detils file
    uname = ''              #file to save the host name 
    vmfsFle = ''

    for path, subdirs, files in os.walk(root):
            for name in files:
                    if fnmatch(name, pattern) and 'prettyPrint.sh_hostlist' in name:
                            print(os.path.join(path, name))
                            hostdtl = os.path.join(path, name)
                    elif fnmatch(name, pattern) and 'uname_-a' in name:
                            uname = os.path.join(path,name)
                    elif fnmatch(name,pattern) and 'localcli_storage-nmp-device-list.txt' in name:
                        data_store_info = os.path.join(path,name)
                    elif fnmatch(name,pattern) and 'localcli_storage-vmfs-extent-list.txt' in name:
                        data_lcl_vmfs = os.path.join(path,name)
                    elif fnmatch(name,pattern) and 'nicinfo.sh.txt' in name:
                        nicinfo_fle = os.path.join(path,name)
                    elif (fnmatch(name,pattern) and 'localcli_storage-core-adapter-list.txt' in name) or (fnmatch(name,'*.json') and 'localcli_storage-core-adapter-list.json' in name):
                        core_adaptr_fle = os.path.join(path,name)
                    elif (fnmatch(name,pattern) and 'localcli_storage-filesystem-list--i.txt' in name):
                        vmfsFle =os.path.join(path,name)
                    # elif 'lockmode' in name:
                    #      print(os.path.join(path,name))

    hostfle = open(hostdtl,'r')
    # print(hostfle)

    hostDetails = {}

    host = False

    # loop to get the name of the host from uname file
    hstdtl = open(uname,'r')
    hstname = ''
    for j in hstdtl.readlines():
        if 'VMkernel' in j:
            j = j.split()[1].split('.')[0]
            # print(j)
            hstname = j

    # loop to get the host details from the pretty file
    for i in hostfle.readlines():
        if hstname in i or host:
            host = True
            if 'hostName' in i:
                i = i.replace('hostName','').replace('/>','').replace('<','').replace('>','')
                # print(i)
                hostDetails['hostName'] = str(i).lstrip().rsplit()[0]
            elif 'ipAddress' in i:
                i = i.replace('ipAddress','').replace('/>','').replace('<','').replace('>','')
                # print(i)
                # print('ipadress')
                hostDetails['ipAddress'] = str(i).lstrip().rsplit()[0]
            elif 'hostdPort' in i:
                i = i.replace('hostdPort','').replace('/>','').replace('<','').replace('>','')
                # print(i)
                hostDetails['hostdPort'] = str(i).lstrip().rsplit()[0]
            elif 'build' in i:
                i = i.replace('build','').replace('/>','').replace('<','').replace('>','')
                # print(i)
                hostDetails['build'] = str(i).lstrip().rsplit()[0]
            elif 'version' in i :
                i = i.replace('version','').replace('/>','').replace('<','').replace('>','')
                hostDetails['version'] = str(i).lstrip().rsplit()[0]
                # print(i)
        
            
            if len(hostDetails) == 5:
                break
            




    # host details are done

    #Now statrting with the device connected data
    # 41766731703f456b764a6f6a
    # 41766731703f456b764a6f6a)

    na_lst_hex = []
    na_lst = []

    data_file = open(data_store_info,'r')

    data_path_plcy_lst = []

    for i in data_file.readlines():
        if 'Device Display Name' in i:
            s = i.split()
            i = s[len(s)-1]
            i = i[5:]
            i = i[:len(i)-1]
            na_lst.append(i)
            s = s[len(s)-1][13:]
            s = s[-2::-1]
            s = s[::-1]
            # s = unicode(s, errors='ignore')
            j = bytes.fromhex(s)
            # print(s)
            na_lst_hex.append(s)
            # print(j)

            #check for path selection policy
        elif 'Path Selection Policy:' in i:
                sl = i.split()[len(i.split())-1]
                data_path_plcy_lst.append(sl)



    data_vmfs_fl = open(data_lcl_vmfs,'r')
    data_vmfs_lst = []

    for i in data_vmfs_fl.readlines():
            for j in na_lst_hex:
                if j in i:
                    i = i.split()
                    data_vmfs_lst.append(i[0])

    # print('Na_list',len(na_lst))
    # print('Na_Hex_list',len(na_lst_hex))
    # print('Policy_path',len(data_path_plcy_lst))
    # print('VMFS',len(data_vmfs_lst))

    # {
    #     'naaid':'',
    #     'srl_nmbr':'',
    #     'pth_plcy':'',
    #     'ats_scsi':''
    # }
    data_lst=[]
    if len(na_lst) == len(na_lst_hex) :
        for i in range(len(na_lst)):
            data_lst.append({
            'naaid':na_lst[i],
            'srl_nmbr':na_lst_hex[i],
            'pth_plcy':data_path_plcy_lst[i],
            })


    # print('VMfs',data_vmfs_lst)


    #Network Information


    #NIC infor
    '''Name
        IP
        MTU'''

    nic_fle = open(nicinfo_fle,'r')
    tbl_data = []
    tbl_strtd = False
    tbl_end = False
    for i in nic_fle.readlines():
        if 'Driver' in i and 'Speed' in i:
            tbl_strtd = True
            # print('started')
        if  i in ['\n', '\r\n'] and tbl_strtd and not tbl_end:
            tbl_end = True
            # print('table ended')
        if tbl_strtd and not tbl_end:
            tbl_data.append(i)
    tbl_hdrs = tbl_data[0].split()
    tbl_dtl = []
    for i in tbl_data[2:]:
        j = i.split()

        print(tbl_hdrs[10], '---', tbl_hdrs[11],'----',j[7])

        tbl_dtl.append({
            tbl_hdrs[0] : j[0],
            tbl_hdrs[1]+tbl_hdrs[2] : j[1],
            tbl_hdrs[3] : j[2],
            tbl_hdrs[4]+tbl_hdrs[5] : j[3],
            tbl_hdrs[6]+tbl_hdrs[7] : j[4],
            tbl_hdrs[8] : j[5],
            tbl_hdrs[9] : j[6],
            tbl_hdrs[10]+tbl_hdrs[11] : j[7],
            tbl_hdrs[12] : j[8],
            tbl_hdrs[13] : ' '.join(j[9:])
        })


    #for core adpter HBA info

    core_adaptr_fl = open(core_adaptr_fle,'r')
    core_hba_adptr = []

    for i in core_adaptr_fl.readlines():
        core_hba_adptr.append(i)

    #lines from vmfs localclistorage file
    #three columns for DSI i.e, 'naaid' objct
    openVMFS = open(vmfsFle,'r')

    vmfsLst = []
    lcnt = 0 # to coiunthe number of lines and start after 2
    print('This is vmfs',vmfsFle)
    for i in openVMFS.readlines():
        lcnt = lcnt + 1

        if lcnt > 2:
            lne = i.split()
            vmfsLst.append({
                'vmfs_nfs':lne[3],
                'size': lne[4],
                'free' : lne[5]
            })


    # complete data
    # print(hostDetails)
    # print(tbl_dtl)
    # print(data_lst)
    # print(len(core_hba_adptr))

    body={
        'host_dtls':hostDetails,
        'nic_info':tbl_dtl,
        'core_adptr':core_hba_adptr,
        'naaid_tbl':data_lst,
        'vmfsLst': vmfsLst
    }

    
    
    return Response(data={
        'code':'200',
        'body':body
    })
# print(hostDetails)

from django.core.mail import EmailMessage


@api_view(['POST'])
def sendEmail(request):
    data = request.data
    email = EmailMessage('Complaint',data['message'],to=['notiffly@gmail.com'])
    email.send()
    return Response(data={
        'code':'200'
    })

#localcli_storage-filesystem-list--i.txt








