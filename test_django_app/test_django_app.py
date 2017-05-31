import sys

sys.path.append('C:\\Users\\Administrator\\code\\PyWebServer\\')


from pwserver.server import BaseServer
from test_django_app import wsgi

def test():
    s = BaseServer(('127.0.0.1', 8091), wsgi.application)
    s.run_server()

if __name__ == '__main__':
    test()

