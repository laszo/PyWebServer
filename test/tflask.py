from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World!'


def wsgiref():
    from wsgiref.simple_server import make_server

    s = make_server('', 8180, app)
    s.serve_forever()


def pws():
    from pwsmodule import pwserver as pw
    # pw.server.launch(('', 8180), app, cfg_file='config.conf')
    pw.launch(('', 8180), app)

if __name__ == '__main__':
    pws()
    # wsgiref()
