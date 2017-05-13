import socket

MAX_READS = 65537
G_response = 'HTTP/1.0 200 OK'
G_content = """

<head>
<title>Hello, world!</title>
</head>
<body>
Hello, world!
</body>
"""
def run_server(address):
    s = socket.socket()
    s.bind(address)
    s.listen(5)
    while True:
        c, a = s.accept()
        print 'Connected from ', a
        c.recv(MAX_READS)
        c.send(G_response + G_content)
        c.close()
    s.close()

def test():
    address = ('', 8000)
    run_server(address)

if __name__ == '__main__':
    test()


