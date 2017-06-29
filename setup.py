from distutils.core import setup
setup(
    name='pwserver',
    version='0.1a1',
    url="https://github.com/laszo/PyWebServer/",
    author="laszo",
    author_email="lasologo@gmail.com",
    license='MIT',
    keywords='wsgi server framework',
    description='PyWebServer is a full Web application stack, including HTTP server,WSGI server and Web framework.',
    packages=['pwserver'],
    package_data={
        'pwserver': ['mime.types'],
    },
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pwserver=pwserver.launch:run',
        ],
    },
)
