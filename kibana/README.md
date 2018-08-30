# Kibana

Provides a graphical UI for the Elasticsearch container.


## Configuration

The actual configuration of Kibana isn't done by code, but rather in the UI itself. The configuration is (and should always be, at its latest state) exported to `data.json`.

Before importing this configuration, make sure you create an index pattern in Kibana. It should have the pattern `logstash-*` and it's **very** important that you give it the ID `logs`.

To import this configuration into a fresh Kibana, go to `Management`, then `Saved Objects` and finally click `Import` and choose the file to import.
