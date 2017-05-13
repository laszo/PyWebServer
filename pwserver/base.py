import socket
import select
import threading
import app

MAX_READS = 65537
G_response = 'HTTP/1.0 200 OK'

def run_server(address):
    s = socket.socket()
    s.bind(address)
    s.listen(5)
    while True:
        rl, wl, el = select.select([s], [], [])
        for r in rl:
            c, a = r.accept()
            print 'Connected from ', a
            t = threading.Thread(target=handle, args=(c,))
            t.start()
    s.close()

def handle(request):
    raw = request.recv(MAX_READS)
    url = parser(raw)
    result = app.app(url)
    request.send(G_response + result)
    request.close()

def parser(request):
    lines = request.split('\r\n')
    first = lines[0]
    words = first.split()
    print words
    if len(words) > 1:
        return words[1]

def test():
    address = ('', 8000)
    run_server(address)

if __name__ == '__main__':
    test()
