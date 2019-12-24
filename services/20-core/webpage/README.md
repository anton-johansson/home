# Webpage

Webpage hosts my personal webpage. Currently, it's not deployed and simply redirects to my Github profile.


## Prepare namespace

We need to create the namespace first, since there are some manual things that needs to be done in the namespace before deploying.

```shell
$ kubectl apply -f 10-namespace
```


## Webpage stage

The real webpage is in the making, and a stage version is deployed. The real webpage requires certain secrets that aren't committed to Git. The secret is created like this:

```shell
kubectl create secret generic webpage-stage-config \
  --namespace webpage \
  --from-literal=gmailPassword=<some-password> \
  --from-literal=spotifyClientID=<some-id> \
  --from-literal=spotifyClientSecret=<some-secret> \
  --from-literal=spotifyRefreshToken=<some-token> \
  --from-literal=steamApiKey=<some-key>
```


## Install

```shell
$ kubectl apply -f 20-deployment.yaml
$ kubectl apply -f 30-service.yaml
$ kubectl apply -f 40-certificate.yaml
$ kubectl apply -f 50-ingress.yaml
```
