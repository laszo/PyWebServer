# PyWebServer
aim to build a 'real' web server from the very beginning in python

下面的命令会同时启动静态文件服务(读取默认配置文件)：

   pwserver static

启动WSGI服务器：

    pwserver -w wsgi_module_path.application_name
    # same to gunicorn: gunicorn wsgi_module_path:application_name

同时启动WSGI服务器和静态文件服务（读取默认配置文件）：

    pwserver static -w wsgi.applicatioin

启动静态文件服务(指定配置文件)：

    pwserver static -f /path/to/config.conf

同时启动WSGI服务器和静态文件服务（指定配置文件）：

    pwserver static -f /path/to/config.conf -w wsgi.applicatioin
