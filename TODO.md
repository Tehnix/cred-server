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



API endpoints
===

| Resource                        | Method | Function  |
|---------------------------------|--------|-----------|
| /auth                           | GET    | Authenticate the client and return a session key |
| /events                         | GET    | Return IDs of all events, ordered by ID descending |
| /events/<int>                   | GET    | Return full information for a specific event |
| /clients                        | GET    | Return IDs of all clients that are active |
| /clients/me                     | GET    | Return information about the client itself |
| /clients/<int>                  | GET    | Return information about a specific client |
| /clients/<int>/events           | GET    | Return IDs of all events from the client  |
| /clients/<int>/events           | POST   | Create a new event associated with the client |
| /clients/<int>/subscribedevents | GET    | Return IDs of all events the client has subscribed to |

Additionally the following query parameters can also be appended to the
resource, for extra fine-tuning. The parameters below work when using GET
requests on the following resources: /events and /clients. And both GET and PUT
on: /clients/<int>/subscribedevents

| Parameter    | Function                                           |
|--------------|----------------------------------------------------|
| full=<bool>  | Return the full information instead of just IDs    |
| before=<int> | Returns IDs lower than <int>                       |
| after=<int>  | Returns IDs higher than <int>                      |
| limit=<int>  | Limit the number of items to <int> items           |
| offset=<int> | Skip <int> number of items before fetching         |

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
