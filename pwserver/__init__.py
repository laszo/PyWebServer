# --encoding:utf8--

"""
启动静态文件服务(读取默认配置文件)：

    pwserver static

启动WSGI服务器：

    pwserver -w wsgi.app

在上面的命令中，`wsgi`是WSGI应用所在的模块，`app`是WSGI应用的名字。如果类比于`gunicorn`，使用gunicorn启动上面的WSGI应用的方式为：

    gunicorn wsgi:app

如果想要同时启动WSGI服务器和静态文件服务：

    pwserver static -w wsgi.app

如果想要启动指定配置文件来替代默认路径的配置文件，采用如下命令：

    pwserver static -f /path/to/config.conf

相应的，同时启动WSGI服务器和指定配置文件的静态文件服务：

    pwserver static -f /path/to/config.conf -w wsgi.app


[PyWebServer]: https://github.com/laszo/PyWebServer
"""

from server import launch
