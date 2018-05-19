# Logstash

Parser for logs, and routes them in a better format into Elasticsearch.


## Parsers

There's one parser for each Docker container. They're found under [pipeline](./pipeline).

[Test grok patterns](http://grokconstructor.appspot.com/do/match) is a good utility to use when building Grok patterns.

There should be atleast one unit test for each parser. The tests are located under [test](./test).
