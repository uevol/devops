import distutils.sysconfig
import sys
import os
from utils import _
import traceback
import cexceptions
import os
import sys
import time
import requests

plib = distutils.sysconfig.get_python_lib()
mod_path="%s/cobbler" % plib
sys.path.insert(0, mod_path)

def register():
    # this pure python trigger acts as if it were a legacy shell-trigger, but is much faster.
    # the return of this method indicates the trigger type
    return "/var/lib/cobbler/triggers/install/pre/*"

def run(api, args, logger):
    objtype = args[0] # "system" or "profile"
    name    = args[1] # name of system or profile
    ip      = args[2] # ip or "?"

    # FIXME: use the logger

    fd = open("/var/log/cobbler/install.log","a+")
    fd.write("%s\t%s\t%s\tstart\t%s\n" % (objtype,name,ip,time.time()))
    data = {'name':name,'ip':ip,"progress":0}
    r = requests.post("http://192.168.3.168:8000/installation/install_pre_post/", data=data)
    fd.write(r.text)
    fd.close()


    return 0