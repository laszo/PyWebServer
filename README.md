# PyWebServer
aim to build a 'real' web server from the very beginning in python

## Usage
usage: 

    pwserver [static [-f PATH]] [-w MODULE_PATH:APP]

    PATH: Your config file path, default /etc/pwserver.conf

    MODULE_PATH: Your module which contains a WSGI application sample: 
        'django.wsgi'
        '../django.wsgi'
        '/user/code/myproject/'

    APP: Your WSGI application name.
