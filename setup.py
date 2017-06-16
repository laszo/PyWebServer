from distutils.core import setup
setup(
    name='pwserver',
    url="http://www.tornadoweb.org/",
    author="laszo",
    author_email="lasologo@gmail.com",
    license='MIT',
    keywords='wsgi server framework',
    install_requires=[],
    packages=['pwserver'],
    version='0.1',
    description='PyWebServer is a full Web application stack, \
        including HTTP server,WSGI server and Web framework.',
    entry_points={
        'console_scripts': [
            'pwserver=launch:run',
        ],
    },
)
