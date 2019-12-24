# Certificate manager

I'm using [cert-manager](https://github.com/jetstack/cert-manager) to automatically get SSL certificates for our ingresses. I configure the certificate manager to use Lets Encrypt as certificate issuer.


## Installation

We use Helm 3 to install cert-manager:

```
$ kubectl apply --validate=false -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.12/deploy/manifests/00-crds.yaml
$ kubectl create namespace cert-manager
$ helm repo add jetstack https://charts.jetstack.io
$ helm install cert-manager jetstack/cert-manager --namespace cert-manager --version v0.12.0 --values helm-values.yaml
$ kubectl apply -f issuers.yaml
```

For any future upgrades, this command can be used:

```
$ helm upgrade cert-manager jetstack/cert-manager --namespace cert-manager --version v0.12.0 --values helm-values.yaml
```

Note: I've disabled the `webhook` component, because I didn't get it to work properly. It's not recommended, but it's viable option. Read more [here](https://cert-manager.io/docs/installation/compatibility/#disabling-webhook).


## Using it

To use dynamic SSL certificates, you create `Certificate` resources. These resources will in turn generate `Secret` resources that you can use in your tls-configuration. Here is an example:

```yaml
---
kind: Certificate
apiVersion: cert-manager.io/v1alpha2
metadata:
  name: some-service
  namespace: test
spec:
  secretName: some-service-certificate
  dnsNames:
    - some-external-domain.com
  issuerRef:
    name: letsencrypt
    kind: ClusterIssuer
    group: cert-manager.io

---
kind: Ingress
apiVersion: networking.k8s.io/v1beta1
metadata:
  name: some-service
  namespace: test
  labels:
    app.kubernetes.io/name: some-service
  annotations:
    kubernetes.io/ingress.class: external
spec:
  rules:
    - host: some-external-domain.com
      http:
        paths:
          - path: /
            backend:
              serviceName: some-service
              servicePort: 8080
  tls:
    - secretName: some-service-certificate
      hosts:
        - some-external-domain.com
```


### Issuers

I have the following cluster issuers:

* `letsencrypt`
* `letsencrypt-staging` (useful only for testing cert-manager upgrades and similar)
