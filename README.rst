====
cred
====
cred (Connected Reactive Electronic Devices), enables you to connect your
electronic devices, in a way so that they can communicate with each other
and react on events happening in the network.

Events can for example be one device turning on, which then sends out a
signal (an event). Others are then able to subscribe to different events,
and can react when they are notified that such an event has occured.


Usage
=====
1. Set up the server by launching `cred-server`
2. Set up each client and configure the events they transmit and subscribe to
3. Enjoy!


API
=====
The URL endpoints and their functionality are described below,

All actors must authenticate first

POST /auth - Authenticate the client and get a session key

General endpoints

GET  /events - Get IDs of all events with newest first
GET  /events?limit=10 - Get the IDs of the last 10 events, can be combined with offset
GET  /events?offset=10 - Get IDs of all events after the 10 first, can be combined with limit
GET  /events?limit=10&offset=10 - Combination of limit and offset on events
GET  /events/<event_id> - Return information about a specific event
GET  /events/full - Return full information about all events. Can also be combined with limit and offset

Client specific endpoints

POST /client/events - Create a new event
GET  /client/events - Get IDs of all events the client has subscribed to, can be combined with offset and limit like /events
GET  /client/events/full - Return full information about all events the client has subscribed to. Can also be combined with offset and limit like /events/full
PUT  /client/events - Get IDs of all new events since the client last pulled for them via this method
PUT  /client/events/full - Return full information of all new events since the client last did a PUT on /client/events


Development
=====
The following should get you running:

1) Set up a virtual environment: `virtualenv env`
2) Activate the virtual environment: `source env/bin/activate`
3) Install the required packages: `pip install -r requirements.txt`
4) Run tests with `nosetests` and alternatively with `--with-watch` (detects file changes)
