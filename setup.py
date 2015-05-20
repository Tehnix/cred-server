""" Setup file for the cred-server package. """
from setuptools import setup
import sys

# The package only works with python >=3.0
if sys.version_info < (3,):
    print("I'm only for 3, please upgrade")
    sys.exit(1)


setup(
    name='cred-server',
    version='0.2.0',
    author='Tehnix',
    author_email='ckl@codetalk.io',
    packages=['cred', 'cred.test'],
    scripts=['bin/cred-server', 'bin/cred-client'],
    url='https://github.com/Tehnix/cred',
    license='BSD',
    description='Connected Reactive Electronic Devices.',
    long_description=open('README.md').read(),
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
    test_suite='nose.collector',
)
