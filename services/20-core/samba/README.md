# Samba share

## Install

```shell
$ kubectl apply -f 10-namespace.yaml
$ kubectl create secret -n samba generic config --from-literal=user=<username>;<password>
$ kubectl apply -f 20-deployment.yaml
```
