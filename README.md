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
Simply install with pip, add a configuration and run it.

1. `$ pip install cred-server`$
3. `$ cred-server`

and test out the API with curl :)


Generating API keys
=====
You can generate API keys with the command line utility `cred-gen`. Make sure
it is using the same configuration as your server. There are three different permission levels,

| Permission | Access                               |
|------------|--------------------------------------|
| admin      | All resources                        |
| write      | All POST and GET except for API keys |
| read       | All GET except for API keys          |

see `cred-gen --help` for more information on how to use the program.


Configuration
=====
If you don't supply the configuration location via `--config=/path/to/config`, then the configuration files are searched for in the following order:
    1. Local directory
    2. Users home directory
    3. Users app directory
    4. System app directory

The file searched for is called credrc for 1., 3. and 4. and.credrc and 2. If none are found, it will use the default configuration.

Example configuration for a local setup with a SQLite3 database:

```yaml
SSL: False
approot: '127.0.0.1'
host: '*'
port: 5000
scheduler: False
pingtimeout: 240
database:
  type: 'sqlite3'
  user: ''
  password: ''
  host: ''
  port: ''
  database: 'cred-server.db'
```

or using PostgreSQL,

```yaml
SSL: False
approot: '127.0.0.1'
host: '*'
port: 5000
scheduler: False
pingtimeout: 240
database:
  type: 'postgresql'
  user: 'scott'
  password: 'tiger'
  host: 'localhost'
  port: '5432'
  database: 'mydatabase'
```


API
=====
The URL endpoints and their functionality are described below,

| Resource                        | Method | Function  |
|---------------------------------|--------|-----------|
| `/auth`                           | GET    | Authenticate the client and return a session key |
| `/events`                         | GET    | Return IDs of all events, ordered by ID descending |
| `/events`                         | POST   | Create a new event associated with the client POSTing it |
| `/events/<int>`                   | GET    | Return full information for a specific event |
| `/clients`                        | GET    | Return IDs of all clients that are active |
| `/clients/me`                     | GET    | Return information about the client itself |
| `/clients/<int>`                  | GET    | Return information about a specific client |
| `/clients/<int>/events`           | GET    | Return IDs of all events from the client  |
| `/clients/<int>/subscribedevents` | GET    | Return IDs of all events the client has subscribed to |

The above resources are accessible with read permissions for all GETs and write for all POSTs and GETs.

| Resource                        | Method | Function |
|---------------------------------|--------|----------|
| `/apikeys`                      | GET    | Return IDs of all API keys |
| `/apikeys`                      | POST   | Generate a new API key |
| `/apikeys/<int>`                | GET    | Return information about a specific API key |

These resources are special, and require admin permissions.

### Parameters

Additionally the following query parameters can also be appended to the
resource, for extra fine-tuning. The parameters below work when using GET
requests on the following resources: /events and /clients,
/clients/<int>/events, /clients/<int>/subscribedevents and /apikeys.

| Parameter      | Function                                           |
|----------------|----------------------------------------------------|
| `full=<bool>`  | Return the full information instead of just IDs    |
| `before=<int>` | Returns IDs lower than <int>                       |
| `after=<int>`  | Returns IDs higher than <int>                      |
| `limit=<int>`  | Limit the number of items to <int> items           |
| `offset=<int>` | Skip <int> number of items before fetching         |


### Example API Call

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


Database
=====
cred uses SQLAlchemy, so it supports the same database that SQLAlchemy does.
The `type` setting in the configuration file takes any value that you can find
at [SQLAlchemy engines](http://docs.sqlalchemy.org/en/latest/core/engines.html "SQLAlchemy engines") (like sqlite3,
postgresql, postgresql+psycopg2, etc.).


Frontend
=====
You can check out [cred-web](https://github.com/Tehnix/cred-web "cred-web repository") for a pure javascript frontend to the API server. It shows the active clients and all the events that are coming in.


Clients
=====
To easily create clients that connect to the API server, you can check out the client library at [cred-client](https://github.com/Tehnix/cred-client "cred-client repository").


Development
=====
The following should get you running:

1. `$ git clone git@github.com:Tehnix/cred-server.git && cd cred-server`
2. `$ virtualenv env && source env/bin/activate`
3. `$ pip install -r requirements.txt`
4. Run tests with `nosetests` and alternatively with `--with-watch` (detects file changes)

or a one-liner,

```bash
$ git clone git@github.com:Tehnix/cred-server.git && cd cred-server && virtualenv env && source env/bin/activate && pip install -r requirements.txt
```
