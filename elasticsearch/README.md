# Elasticsearch

Documentation and code for the Elasticsearch node


## Notes

The `vm.max_map_count` kernel setting needs to be set to at least `262144` for production use. Add `vm.max_map_count=262144` to `/etc/sysctl.conf` to add it permanently and run `sysctl -w vm.max_map_count=262144` to set the value live.

More information about the setup can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html).
