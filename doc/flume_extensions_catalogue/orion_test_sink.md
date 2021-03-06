#<a name="top"></a>OrionTestSink
Content:

* [Functionality](#section1)
    * [Mapping NGSI events to flume events](#section1.1)
    * [Mapping Flume events to logs](#section1.2)
    * [Example](#section1.3)
* [Administration guide](#section2)
    * [Configuration](#section2.1)
    * [Use cases](#section2.2)
    * [Important notes](#section2.3)
        * [About batching](#section2.3.1)

##<a name="section1"></a>Functionality
`com.iot.telefonica.cygnus.sinks.OrionTestSink`, or simply `OrionTestSink` is a sink designed to test Cygnus when receiving NGSI-like context data events. Usually, such a context data is notified by a [Orion Context Broker](https://github.com/telefonicaid/fiware-orion) instance, but could be any other system speaking the <i>NGSI language</i>.

Independently of the data generator, NGSI context data is always transformed into internal Flume events at Cygnus sources. In the end, the information within these Flume events is not meant to be persisted at any real storage, but simply logged (depending on your `log4j` configuration, the logs will be printed in console, a file...).

Next sections will explain this in detail.

[Top](#top)

###<a name="section1.1"></a>Mapping NGSI events to flume events
Notified NGSI events (containing context data) are transformed into Flume events (such an event is a mix of certain headers and a byte-based body), independently of the NGSI data generator or the final backend where it is persisted.

This is done at the Cygnus Http listeners (in Flume jergon, sources) thanks to [`OrionRestHandler`](./orion_rest_handler.md). Once translated, the data (now, as a Flume event) is put into the internal channels for future consumption (see next section).

[Top](#top)

###<a name="section1.2"></a>Mapping Flume events lo logs
The mapping is direct, converting the context data into strings to be written in console, or file...

[Top](#top)

###<a name="section1.3"></a>Example
Assuming the following Flume event is created from a notified NGSI context data (the code below is an <i>object representation</i>, not any real data format):

    flume-event={
        headers={
	         content-type=application/json,
	         timestamp=1429535775,
	         transactionId=1429535775-308-0000000000,
	         ttl=10,
	         fiware-service=vehicles,
	         fiware-servicepath=4wheels,
	         notified-entities=car1_car
	         notified-servicepaths=4wheels
	         grouped-entities=car1_car
	         grouped-servicepath=4wheels
        },
        body={
	         entityId=car1,
	         entityType=car,
	         attributes=[
	             {
	                 attrName=speed,
	                 attrType=float,
	                 attrValue=112.9
	             },
	             {
	                 attrName=oil_level,
	                 attrType=float,
	                 attrValue=74.6
	             }
	         ]
	     }
    }

Assuming the log appender is the console, then `OrionTestSink` will log the data within the body as:

```
time=2015-12-10T14:31:49.389CET | lvl=INFO | trans=1429535775-308-0000000000 | srv=vehicles | subsrv=4wheels | function=getEvents | comp=Cygnus | msg=com.telefonica.iot.cygnus.handlers.OrionRestHandler[150] : Starting transaction (1429535775-308-0000000000)
time=2015-12-10T14:31:49.392CET | lvl=INFO | trans=1429535775-308-0000000000 | srv=vehicles | subsrv=4wheels | function=getEvents | comp=Cygnus | msg=com.telefonica.iot.cygnus.handlers.OrionRestHandler[232] : Received data ({  "subscriptionId" : "51c0ac9ed714fb3b37d7d5a8",  "originator" : "localhost",  "contextResponses" : [    {      "contextElement" : {        "attributes" : [          {            "name" : "speed",            "type" : "float",            "value" : "112.9"          },          {            "name" : "oil_level",            "type" : "float",            "value" : "74.6"          }        ],        "type" : "car",        "isPattern" : "false",        "id" : "car1"      },      "statusCode" : {        "code" : "200",        "reasonPhrase" : "OK"      }    }  ]})
time=2015-12-10T14:31:49.394CET | lvl=INFO | trans=1429535775-308-0000000000 | srv=vehicles | subsrv=4wheels | function=getEvents | comp=Cygnus | msg=com.telefonica.iot.cygnus.handlers.OrionRestHandler[255] : Event put in the channel (id=1491400742, ttl=10)
time=2015-12-10T14:31:49.485CET | lvl=INFO | trans=1429535775-308-0000000000 | srv=vehicles | subsrv=4wheels | function=persistAggregation | comp=Cygnus | msg=com.telefonica.iot.cygnus.sinks.OrionTestSink[176] : [test-sink] Persisting data at OrionTestSink. Data (Processing event={Processing headers={recvTimeTs= 1429535775, fiwareService=vehicles, fiwareServicePath=4wheels, destinations=car1_car}, Processing context element={id=car1, type=car}, Processing attribute={name=speed, type=float, value="112.9", metadata=[]}, Processing attribute={name=oil_level, type=float, value="74.6", metadata=[]}})
time=2015-12-10T14:31:49.486CET | lvl=INFO | trans=1429535775-308-0000000000 | srv=vehicles | subsrv=4wheels | function=process | comp=Cygnus | msg=com.telefonica.iot.cygnus.sinks.OrionSink[178] : Finishing transaction (1429535775-308-0000000000)
```

[Top](#top)

##<a name="section2"></a>Adinistration guide
###<a name="section2.1"></a>Configuration
`OrionTestSink` is configured through the following parameters:

| Parameter | Mandatory | Default value | Comments |
|---|---|---|---|
| type | yes | N/A | Must be <i>com.telefonica.iot.cygnus.sinks.OrionTestSink</i> |
| channel | yes | N/A |
| enable_grouping | no | false | <i>true</i> or <i>false</i> |
| data_model | no | dm-by-entity |  Always <i>dm-by-entity</i>, even if not configured |
| batch_size | no | 1 | Number of events accumulated before persistence |
| batch_timeout | no | 30 | Number of seconds the batch will be building before it is persisted as it is |

A configuration example could be:

    cygnusagent.sinks = test-sink
    cygnusagent.channels = test-channel
    ...
    cygnusagent.sinks.test-sink.type = com.telefonica.iot.cygnus.sinks.OrionTestSink
    cygnusagent.sinks.test-sink.channel = ckan-channel
    cygnusagent.sinks.test-sink.enable_grouping = false
    cygnusagent.sinks.test-sink.data_model = dm-by-entity
    cygnusagent.sinks.test-sink.batch_size = 100
    cygnusagent.sinks.test-sink.batch_timeout = 30

[Top](#top)

[Top](#top)

###<a name="section2.2"></a>Use cases
Use this sink in order to test if a Cygnus deployment is properly receiveing notifications from an Orion Context Broker premise.

[Top](#top)

###<a name="section2.3"></a>Important notes
####<a name="section2.3.1"></a>About batching
`OrionTestSink` extends `OrionSink`, which provides a batch-based built-in mechanism for collecting events from the internal Flume channel. This mechanism allows extending classes have only to deal with the persistence details of such a batch of events in the final backend.

What is important regarding the batch mechanism is it largely increases the performance of the sink, because the number of writes is dramatically reduced. Particularly, this is not important for this test sink, but the other sinks will largely benefit from this feature. Please, check the specific sink documentation for more details.

[Top](#top)
