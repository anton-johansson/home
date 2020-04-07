# Callback proxy service

The callback proxy service is useful when working with 3rd party APIs that utilize callbacks/webhooks.


## Install

Pre-configure the `config.yaml` file. It contains secrets, so it cannot be in source control, and is ignored by Git.

```shell
$ kubectl create namespace callback-proxy-service
$ kubectl create configmap config --namespace callback-proxy-service --from-file ./config.yaml
$ kubectl apply -f callback-proxy-service.yaml
```
