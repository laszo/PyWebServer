PyWebServer
===========

Aim to build a 'real' web server from the very beginning in python

Installation
------------

PyWebServer requires Python 2.x >= 2.6.

Install from archive file (it hasn't been uploaded to PyPI yet):

    $ pip install https://github.com/laszo/PyWebServer/archive/v0.1.zip

Usage
-----

Serving static files:
---------------------

    $ pwserver static [-f PATH]

Configuration file format is [nginx like](http://nginx.org/en/docs/beginners_guide.html):

    http {
        server {
            listen 8081;
            location / {
                root /Users/data/www;
            }
        }
        server {
            listen 8082;
            location /static/ {
                root /Users/data/static;
            }
        }
    }

Default config file is at `/etc/pwserver.conf`. 

Serving WSGI Application
------------------------

If you have a WSGI application at `hello.py`:

.. code-block:: python
    def demoapp(env, start_response):
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['hello, world']

You can serving it by:

    $ pwserver -w hello:demoapp


Full Usage
----------

    ------------------------------------------------------------------------------
    usage: pwserver [-h || --help] [static [-f PATH]] [-w MODULE_PATH:APP [-a ADDRESS]] 

    -h                  :  Show usage and return (also --help).

    static [-f PATH]    : serving as a static file server. PATH is Your config file path, default /etc/pwserver.conf

    -w                  : serving as a WSGI server. MODULE_PATH: Your module which contains a WSGI application. APP: Your WSGI application name.
    -a                  : ADDRESS: WSGI server address.
    ------------------------------------------------------------------------------
