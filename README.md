cred
====
**cred** (Connected Reactive Electronic Devices), enables you to connect your
electronic devices, in a way so that they can communicate with each other
and react on events happening in the network.


An example application cred would be to connect the devices in a living room. If the light switch is connected, and then turned on it would transmit an event like,

```JSON
{
    "device": "Light",
    "location": "Living Room",
    "action": "Toggled",
    "value": "On"
}
```

which the thermostat would have subscribe to. The server will then transmit this event to the thermostat when it occurs, and the thermostat could act accordingly, like say turning up the temperature in the room since it's most likely going to be occupied now.

Usage
=====
Currently not complete, but you can

1. `$ git clone git@github.com:Tehnix/cred.git`
2. `$ cd cred && python cred/runserver.py`

and test out the API with curl :)


API
=====
The URL endpoints and their functionality are described below,

| Resource                        | Method | Function  |
|---------------------------------|--------|-----------|
| `/auth`                           | GET    | Authenticate the client and return a session key |
| `/events`                         | GET    | Return IDs of all events, ordered by ID descending |
| `/events/<int>`                   | GET    | Return full information for a specific event |
| `/clients`                        | GET    | Return IDs of all clients that are active |
| `/clients/me`                     | GET    | Return information about the client itself |
| `/clients/<int>`                  | GET    | Return information about a specific client |
| `/clients/<int>/events`           | GET    | Return IDs of all events from the client  |
| `/clients/<int>/events`           | POST   | Create a new event associated with the client |
| `/clients/<int>/subscribedevents` | GET    | Return IDs of all events the client has subscribed to |

Additionally the following query parameters can also be appended to the
resource, for extra fine-tuning. The parameters below work when using GET
requests on the following resources: /events and /clients. And both GET and PUT
on: /clients/<int>/subscribedevents

| Parameter      | Function                                           |
|----------------|----------------------------------------------------|
| `full=<bool>`  | Return the full information instead of just IDs    |
| `before=<int>` | Returns IDs lower than <int>                       |
| `after=<int>`  | Returns IDs higher than <int>                      |
| `limit=<int>`  | Limit the number of items to <int> items           |
| `offset=<int>` | Skip <int> number of items before fetching         |

An example call with multiple parameters `/events?full=true&limit=10&offset=10`,
which will pull the full information for 10 events, starting from after the 10
newest ones. This can be useful if you want to be able to pull all events and
paginate them, or something like that. To get the next page, you would then add
the `&from=` parameter, with the first ID you got back, and increment the offset
with 10 more.

Alternatively, something like `/clients/<int>/events?full=true` can be used to
pull the full information for new events that the client has subscribed to.

With the `after=<int>` parameter, the server now doesn't need to keep track of
when the client last pulled, since the client can control that itself. To give
an example, a client with ID=145 is doing its first series of requests:

1. The client requests `/clients/145/subscribedevents?full=true&limit=10`
2. A response with a list of events comes back, the newest being ID=288
3. The client requests `/clients/145/subscribedevents?from=true&after=288`
4. A response with all events with ID > 288 comes back

And so on. The minimizes the state kept on the server. If step 2. produced no
results, the client would set `after=0`, which would still give new events only.


Development
=====
The following should get you running:

1. Set up a virtual environment: `virtualenv env`
2. Activate the virtual environment: `source env/bin/activate`
3. Install the required packages: `pip install -r requirements.txt`
4. Run tests with `nosetests` and alternatively with `--with-watch` (detects file changes)
