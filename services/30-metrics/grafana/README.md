# Prometheus

Prometheus is in charge of gathering metrics by scraping various endpoints.


## Installation

First, we need to create the namespace:

```shell
$ kubectl apply -f 10-namespace.yaml
```

Then we need to create our secret Home Assistant access token that Prometheus will use:

```shell
$ kubectl create secret -n prometheus generic home-assistant-access-token --from-literal=token=<long lived access token>
```

Then we can apply the rest of the manifests:

```shell
$ kubectl apply -f 20-config.yaml
```
