====
cred
====

This package uses type annoations, and therefore requires python >=3.0. 
This makes the package type checkable, using mypy-lang[0].

cred (Connected Reactive Electronic Devices), enables you to connect your 
electronic devices, in a way so that they can communicate with each other
and react on events happening in the network. 

Events can for example be one device turning on, which then sends out a 
signal (an event). Others are then able to subscribe to different events, 
and can react when they are notified that such an event has occured.


[0] http://www.mypy-lang.org


Usage
=====

First, get a server running. Then connect each device to the server, while
also registrering what events they react to, and what they are capable of
themselves.


Development
=====
The following should get you running:

1) Set up a virtual environment: `virtualenv env`
2) Activate the virtual environment: `source env/bin/activate`
3) Install the required packages: `pip install -r requirements.txt`
4) Run tests with `nosetests` and alternatively with `--with-watch` (detects file changes)
5) Run pylint with `pylint cred`
