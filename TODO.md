Programming
===
## Server
* API only approach!
* Implement the endpoints specified in `routes.py`
* A way to generate API keys

## Web Client
* Javascript frontend that uses the API and displays it nicely
* Either use a *very* simply framework, or just do it with JQuery
* Having a self updating list of events that come in and clients that are online
* Click in on a client and see what events that client has sent, and the events
  the client has subscribed to

## Client
* A python class, that the implementer will subclass
* Shall handle everything, and the implementer must only implement some abstract
functions
* Make it read user input to simulate events
* Make it output subscribed events



Writing
===
* Completely rewrite `Architecture` chapter
    * Note that we're going back to server + client
* Update/rewrite `Specification` chapter
    * Include a quick overview of the URL endpoints in the beginning
