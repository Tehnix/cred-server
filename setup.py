""" Setup file for the cred-server package. """
from setuptools import setup
import sys

# The package only works with python >=3.0
if sys.version_info < (3,):
    print("I'm only for 3, please upgrade")
    sys.exit(1)

version = '0.2.18'

setup(
    name='cred-server',
    version=version,
    author='Tehnix',
    author_email='ckl@codetalk.io',
    packages=[
        'cred',
        'cred.models',
        'cred.resources',
        'cred.common',
        'cred.test'
    ],
    scripts=['bin/cred-server', 'bin/cred-gen'],
    url='https://github.com/Tehnix/cred-server',
    download_url='https://github.com/Tehnix/cred-server/tarball/v{0}'.format(version),
    license='BSD',
    description='Connected Reactive Electronic Devices.',
    # long_description=open('README.md').read(),
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
    install_requires=[
        'Flask>=0.10.1',
        'Flask-RESTful>=0.3.2',
        'Flask-SQLAlchemy',
        'Flask-CORS>=2.0.1',
        'Flask-Testing>=0.4.2',
        'pyOpenSSL',
        'PyYAML',
        'appdirs',
    ],
    test_suite='nose.collector',
)
