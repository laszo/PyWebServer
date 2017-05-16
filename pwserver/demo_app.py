#! -- encoding:utf-8 --
import base_server

G_content = """

<head>
<title>Hi</title>
</head>
<body>
Hi, %s.
</body>
    """

def hello(name):
    return G_content % name

def index(*args):
    return G_content % 'User'

# urlpatterns 中的group数量必须与函数定义的参数数量一致
# 使用框架，要遵守框架的规则，否则写框架的人很难做

urlspatterns = [
    (r'^/$', index),
    (r'^/hello\?user=(?P<name>\D+)', hello),
    (r'^/hello\?user=(\D+)&age=(\d+)', hello),
    (r'^/hello\?(\S+=\S+)&(\S+=\S+)', hello),
]

def test():
    app = base_server.application(('', 8009), urlspatterns)
    base_server.run_server(app)

if __name__ == '__main__':
    test()

