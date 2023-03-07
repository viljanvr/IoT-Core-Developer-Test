# IoT Core Developer Test submission

**This is a basic Django application that I've developed for the IoT Core Developer Test case. As specified in the case description, the application consumes data from the MQTT server `mqtt.hsl.fi`, and makes the data available through a REST API. The MQTT server provides high-frequency positioning data for public transport vehicles in the Helsinki-area. This is my first time writing a Django application, so this is only a proof of concept with limited functionality.**

The database model for this application consist of a single table with the following attributes: _busID_, _route_, _operator_, _location_, _updated_ and _lastStop_. If we where to extend the fuctionality of this application it would obvisoly not be a good solution, but since this only is for demonstrational purposes, the single table will do just fine.

I've chosen to use a _SpatiaLite_-database that extends SQLite to support spatial SQL capabilities. This enables us to easily calculate the distance between two coordniates, and we can therefore have API calls that get busses within a certain radius from a given coordinate.

The applications subscribes to the `vp`-events (vehicle position) from the MQTT server to update the position of each bus. When a new position is given, the previous position is overwritten. In other words, no location history is currently stored. The application also subscribes to `dep`-events (Vehicle departs from a stop and leaves the stop radius) from the MQTT-server. This is to update the lastStop attribute. A `vjout`-event (Vehicle signs off from a service journey, after reaching the final stop) is used to delete the bus from the database, since it's not needed anymore.

One feature that currently isn't implemented is to get the next stop of a given bus. Since the MQTT server doesn't provide route information, the [Routing API](https://digitransit.fi/en/developers/apis/1-routing-api/routes/) from digitransit can be used. More specifically the **fuzzyTrip** query type will provide the details of a given bus trip ([more information availble here](https://digitransit.fi/en/developers/apis/1-routing-api/routes/#a-namefuzzytripaquery-a-trip-without-its-id)). A possible implementation would be to subscribe to `vja`-events from the MQTT server. A `vja`-event is published when a vehicle starts on a trip. When such an event occurs, we could use the fuzzyTrip query to get and save information about the bus stops for the trip of the given bus.

To solve the case I've used the high-frequency positioning API docs: [https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/](https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/)

To start the surver run the following command:

```shell
python3 ./manage.py runserver
```

---

## API

### Get a bus by it's ID (GET)

To get a bus by it's ID use a GET request to the following endpoint `bus/{bus_ID}/`

_Example:_

```shell
curl -X GET http://127.0.0.1:8000/bus/14/
```

_Result:_

```json
{
    "busID": 14,
    "route": "611",
    "operator": 30,
    "location": "SRID=4326;POINT (24.960159 60.258053)",
    "updated": "2023-03-07T17:34:00.889000Z",
    "lastStop": 1353122
}
```

### Get all busses (GET)

To get all busses use a GET request to the `bus/`-endpoint.

_Example:_

```shell
curl -X GET http://127.0.0.1:8000/bus/
```

_Result:_

```json
[
    {
    "busID": 1164,
    "route": "510",
    "operator": 22,
    "location": "SRID=4326;POINT (60.19094 24.923005)",
    "updated": "2023-03-07T16:27:34.112000Z",
    "lastStop": 1180121
  },
  {
    "busID": 1171,
    "route": "42",
    "operator": 22,
    "location": "SRID=4326;POINT (24.89921 60.205673)",
    "updated": "2023-03-07T17:33:52.480000Z",
    "lastStop": 1160206
  },
  [...]
]
```

### Get busses within a certain radius (POST)

To get all busses within a certain radius use a POST request to the `bus/`-endpoint with the following form-data:

-   `latitude` in decimal degrees (WGS 84 format)
-   `longitude` in decimal degrees (WGS 84 format)
-   `radius` in meters

The API will also return a distance in meters from each bus to the given coordinate.

_Example:_

```shell
curl -X POST http://127.0.0.1:8000/bus/
    -F latitude=60.289812
    -F longitude=24.946788
    -F radius=1000
```

_Result:_

```json
[
  {
    "busID": 24,
    "distance": 0,
    "route": "584",
    "operator": 17,
    "location": "SRID=4326;POINT (24.946788 60.289812)",
    "updated": "2023-03-07T17:33:52.512000Z",
    "lastStop": 4510240
  },
  {
    "busID": 1074,
    "distance": 175.6995945764203,
    "route": "572",
    "operator": 22,
    "location": "SRID=4326;POINT (24.949969 60.289918)",
    "updated": "2023-03-07T17:33:33.857000Z",
    "lastStop": null
  },
  [...]
]
```

---
