#!/usr/bin/python
import importlib
import multiprocessing
import os
import sys
import threading

import tools as t
from server import ConfigServer, WSGIServer

DEFAULT_CONFIG_FILE = '/etc/pwserver.conf'
DEFAULT_WSGI_ADDRESS = ('', 8180)

USEAGE = """
------------------------------------------------------------------------------
usage: pwserver [-h || --help] [static [-f PATH]] [-w MODULE_PATH:APP [-a ADDRESS]] 

-h                  :  Show usage and return (also --help).

static [-f PATH]    : serving as a static file server. PATH is Your config file path, default /etc/pwserver.conf

-w                  : serving as a WSGI server. MODULE_PATH: Your module which contains a WSGI application. APP: Your WSGI application name.
-a                  : ADDRESS: WSGI server address.
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
    if wsgiapp:
        if not address:
            address = DEFAULT_WSGI_ADDRESS
        # runwsgi(address, wsgiapp)
        worker = threading.Thread(target=runwsgi, args=(address, wsgiapp, ))
        worker.start()

def runserver(config):
    server = ConfigServer(config=config)
    server.run_server()

def findapp(apppath):
    try:
        parts = apppath.split(":", 1)
        if len(parts) == 1:
            module, obj = apppath, "application"
        else:
            module, obj = parts[0], parts[1]
        mpath = '/'.join(module.split('/')[:-1])
        sys.path.append(os.path.realpath(mpath))
        module = module.split('/')[-1]

        importlib.import_module(module)
        mod = sys.modules[module]

        app = eval(obj, vars(mod))

        return app
    except Exception:
        msg = "Failed to find application."
        raise

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
    if alen == 1:
        show_useage()

    if '-h' in argv or '--help' in argv:
        show_useage()
        return

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
    elif '-w' in argv:
        res = find_after_arg(argv, '-w', 'WSGI application')
        if res:
            if '-a' in argv:
                add = find_after_arg(argv, '-a', 'WSGI serving address')
                if not add:
                    return
            else:
                add = DEFAULT_WSGI_ADDRESS
            launch(address=add, wsgiapp=res)
        else:
            return
    else:
        show_useage()

if __name__ == '__main__':
    run()
