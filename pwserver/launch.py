#!/usr/bin/python
import sys, os
import multiprocessing
import threading
import tools as t
from server import ConfigServer, WSGIServer

DEFAULT_CONFIG_FILE = '/etc/pwserver.conf'

USEAGE = """
------------------------------------------------------------------------------
usage: pwserver [static [-f PATH]] [-w MODULE_PATH:APP]

PATH: Your config file path, default /etc/pwserver.conf

MODULE_PATH: Your module which contains a WSGI application sample: 
    'django.wsgi'
    '../django.wsgi'
    '/user/code/myproject/'

APP: Your WSGI application name.
------------------------------------------------------------------------------
"""

def show_useage():
    print USEAGE

def launch(address=None, wsgiapp=None, cfg_file=None):
    if cfg_file:
        config = t.config(cfg_file)
        servers = config.find('http.server')
        for server in servers:
            worker = multiprocessing.Process(target=runserver, args=(server, ))
            worker.start()
    if address and wsgiapp:
        # runwsgi(address, wsgiapp)
        worker = threading.Thread(target=runwsgi, args=(address, wsgiapp, ))
        worker.start()

def runserver(config):
    server = ConfigServer(config=config)
    server.run_server()

def findapp(apppath):
    # try:
    parts = apppath.split(":", 1)
    if len(parts) == 1:
        module, obj = apppath, "application"
    else:
        module, obj = parts[0], parts[1]
    mpath = '/'.join(module.split('/')[:-1])
    sys.path.append(os.path.realpath(mpath))
    module = module.split('/')[-1]
    mod = sys.modules[module]
    print os.path.realpath(mpath)
    print module
    print mod
    app = eval(obj, vars(mod))
    print app
    return app
    # except Exception:
    #     msg = "Failed to find application."
    #     raise

def runwsgi(address, wsgiapp):
    app = findapp(wsgiapp)
    server = WSGIServer(address, app)
    server.run_server()

def find_after_arg(argv, arg, argname):
    sidx = argv.index(arg)
    alen = len(argv)
    if alen > sidx + 1:
        return argv[sidx+1]
    show_useage()
    print 'you use the %s arg, but not provide the %s path' % (arg, argname)

def run():
    argv = sys.argv
    alen = len(argv)
    if 'static' in argv:
        cfgfile = DEFAULT_CONFIG_FILE
        sidx = argv.index('static')
        if alen > sidx + 1:
            if argv[sidx+1] == '-f':
                res = find_after_arg(argv, '-f', 'config file')
                if res:
                    cfgfile = res
                else:
                    return
        if os.path.exists(cfgfile):
            launch(cfg_file=cfgfile)
        else:
            print 'config not found: %s' % cfgfile
    if '-w' in argv:
        res = find_after_arg(argv, '-w', 'WSGI application')
        if res:
            launch(address=('', 8180), wsgiapp=res)
        else:
            return

if __name__ == '__main__':
    run()
