from pw_wsgi_server import BaseServer

def flask():
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, flask World!'

    s = BaseServer(('127.0.0.1', 8097), app)
    s.run_server()

if __name__ == '__main__':
    flask()
