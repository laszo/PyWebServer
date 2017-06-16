#!/usr/bin/python
import sys
import os

USEAGE = """
------------------------------------------------------------------------------
usage: pwserver [static [-f PATH]] [-w WSGI_PATH]

PATH: Your config file path, default /etc/pwserver.conf

WSGI_PATH: Your WSGI application path, sample: 
    'django.wsgi.application'
    '../django.wsgi.application'
    '/user/code/myproject/django.wsgi.application'
------------------------------------------------------------------------------
"""

def run():
    argv = sys.argv
    alen = len(argv)
    print 'your argv is: %s, count is %d' % (' '.join(argv), alen)
    if 'static' in argv:
        cfgfile = '/etc/pwserver.conf'
        sidx = argv.index('static')
        print 'static arg at index: %d' % sidx
        if alen > sidx + 1:
            if argv[sidx+1] == '-f':
                res = find_after_arg(argv, '-f')
                if res:
                    cfgfile = res
                else:
                    print 'you use the -f arg, but not provide the config path'
                    show_useage()
                    return
        if os.path.exists(cfgfile):
            serve_static(cfgfile)
        else:
            print 'config not found: %s' % cfgfile
    if '-w' in argv:
        res = find_after_arg(argv, '-w')
        if res:
            serve_wsgi(res)
        else:
            print 'you use the -w arg, but not provide the WSGI application path'
            show_useage()

def serve_wsgi(wsgi):
    print 'serving wsgi: %s' % wsgi

def serve_static(path):
    print '.....'
    print 'Serving static file, using config file: %s' % os.path.realpath(path)

def show_useage():
    print USEAGE

def find_after_arg(argv, arg):
    sidx = argv.index(arg)
    alen = len(argv)
    if alen > sidx + 1:
        return argv[sidx+1]

if __name__ == '__main__':
    run()
