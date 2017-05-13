# from pwserver import run_server

G_content = """

<head>
<title>Hello, world!</title>
</head>
<body>
%s, world!
</body>
"""

def hello1():
    return G_content % 'hello1'

def hello2():
    return G_content % 'hello2'

urls = [
    ('/', hello1),
    ('/hello1', hello1),
    ('/hello2', hello2),
]

def app(url):
    import re
    reg = re.compile(url)
    for u, f in urls:
        if reg.match(u):
            return f()

