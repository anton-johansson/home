# Home Assistant

## z-Wave JS server

After creating the namespace, we need to create some secrets for the Z-Wave JS server:

```sh
$ kubectl create secret -n home-assistant generic zwave-js-server-keys --from-literal=s2-access-control-key=... --from-literal=s2-authenticated-key=... --from-literal=s2-unauthenticated-key=... --from-literal=s0-legacy-key=...
```
