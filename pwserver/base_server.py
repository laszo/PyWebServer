import socket
import select
import threading
from pw_framework import application
import BaseHTTPServer

MAX_READS = 65537
G_response = 'HTTP/1.0 200 OK'
G_404response = """HTTP/1.0 404 Not Found


<head>
<title>Not Found</title>
</head>
<body>
<h1> 404 Not Found.</h1>
</body>
"""

def run_server(app):
    s = socket.socket()
    s.bind(app.address)
    s.listen(5)
    while True:
        rl, wl, el = select.select([s], [], [])
        for r in rl:
            c, a = r.accept()
            print 'Connected from ', a
            t = threading.Thread(target=handle, args=(c, app, ))
            t.start()
    s.close()

def handle(request, app):
    raw = request.recv(MAX_READS)
    url = parser(raw)
    result = app.handle(url)
    if result:
        request.send(G_response + result)
    else:
        request.send(G_404response)
    request.close()

def parser(request):
    lines = request.split('\r\n')
    first = lines[0]
    words = first.split()
    print words
    if len(words) > 1:
        return words[1]


