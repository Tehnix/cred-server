""" Setup file for the cred package. """
from distutils.core import setup

setup(
    name='cred',
    version='0.1.0',
    author='Tehnix',
    author_email='christianlaustsen@gmail.com',
    packages=['cred', 'cred.test'],
    scripts=['bin/cred-server.py', 'bin/cred-client.py'],
    url='http://pypi.python.org/pypi/cred/',
    license='LICENSE',
    description='Connected Reactive Electronic Devices.',
    long_description=open('README.rst').read(),
    install_requires=[],
)

