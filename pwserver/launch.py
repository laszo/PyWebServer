import multiprocessing
import threading
import tools as t
from server import ConfigServer, WSGIServer

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

def runwsgi(address, wsgiapp):
    server = WSGIServer(address, wsgiapp)
    server.run_server()