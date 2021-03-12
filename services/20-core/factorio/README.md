# Factorio

This is a deployment for a Factorio game server.


## Install

```shell
$ kubectl apply -f manifest.yaml
```


## Preparations

The node requires a directory - `/opt/factorio` - that will hold game saves and such. Otherwise, this would all be lost if the `Pod` is recreated.
