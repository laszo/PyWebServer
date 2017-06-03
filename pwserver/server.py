# --encoding:utf-8--
import socket
import select
import threading
import os
import sys
import handler

class BaseServer(object):

    MAX_READS = 65537

    def __init__(self, address, handlercls=handler.handler, wsgiapp=None):
        self.socket = socket.socket()
        self.address = address
        self.handlercls = handlercls
        self.wsgiapp = wsgiapp

    def run_server(self):
        try:
            self.socket.bind(self.address)
            self.socket.listen(5)

            host, port = self.socket.getsockname()[:2]
            # self.server_name = socket.getfqdn(host)
            self.server_name = host
            self.server_port = port

            print 'Server listen at %s:%s' % (self.server_name, str(self.server_port))
        except socket.error as error:
            print 'Server Error:' + error.message
            self.colse_server()
            return

        try:
            self.waiting_request()
        except KeyboardInterrupt:
            self.colse_server()
        finally:
            self.colse_server()

    def waiting_request(self):
        print 'Waiting request...'
        while True:
            rl, wl, el = select.select([self.socket], [], [])
            for r in rl:
                c, a = r.accept()
                print 'Get request at %s:%s' % c.getsockname()[:2]
                self.handle_request(c)
                # t = threading.Thread(target=self.handle, args=(c, self.wsgi_app, ))
                # t.start()

    def handle_request(self, c):
        if self.handlercls:
            handler = self.handlercls(c)
            handler.handle()

    def colse_server(self):
        print 'Server is about to close...'
        self.socket.close()

