# Testing the Logstash pipelines

Contains code and data for verifying the logstash pipelines.

Much of the code and inspiration is taken from [this blog post](https://blog.codecentric.de/en/2016/06/automatic-testing-logstash-configuration/) and [the related GitHub repository](https://github.com/rfalke/testing-logstash-configuration)


## Running

```shell
$ sudo ./run.sh
```


## Grok pattern test logs

#### Elasticsearch

```
[2018-12-05T20:40:30,965][INFO ][o.e.c.r.a.AllocationService  ] [orNxHV6  ] updating number_of_replicas to [0] for indices [.kibana_1]
[2018-12-05T20:40:30,965][INFO][o.e.c.r.a.AllocationService] [orNxHV6] updating number_of_replicas to [0] for indices [.kibana_1]
[2018-12-05T21:16:10,124][INFO ][o.e.c.m.MetaDataCreateIndexService] [orNxHV6] [logstash-2018.12.03] creating index, cause [auto(bulk api)], templates [logstash], shards [1]/[0], mappings []
[2018-12-05T21:16:10,774][INFO ][o.e.c.m.MetaDataMappingService] [orNxHV6] [logstash-2018.12.05/eF9u32mySjynZGj306CU6g] update_mapping [doc]
```

#### Logstash
```
[2018-12-05T21:22:37,118][INFO ][logstash.setting.writabledirectory] Creating directory {:setting=>\"path.dead_letter_queue\", :path=>\"/usr/share/logstash/data/dead_letter_queue\"}
[2018-12-05T21:22:43,997][INFO ][logstash.outputs.elasticsearch] Attempting to install template {:manage_template=>{\"index_patterns\"=>[\"*beat-*\"], \"settings\"=>{\"number_of_shards\"=>1, \"number_of_replicas\"=>0}}}
```
