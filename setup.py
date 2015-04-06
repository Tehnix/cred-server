""" Setup file for the cred package. """
from distutils.core import setup
import sys

# The package only works with python >=3.0
if sys.version_info < (3,):
    print("I'm only for 3, please upgrade")
    sys.exit(1)


setup(
    name='cred',
    version='0.1.3',
    author='Tehnix',
    author_email='christianlaustsen@gmail.com',
    packages=['cred', 'cred.test'],
    scripts=['bin/cred-server', 'bin/cred-client'],
    url='http://pypi.python.org/pypi/cred/',
    license='BSD',
    description='Connected Reactive Electronic Devices.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Home Automation',
    ],
    requires=[
        'python (>=3.0)',
    ],
)

