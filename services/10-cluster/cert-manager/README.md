# Certificate manager

I'm using [cert-manager](https://github.com/jetstack/cert-manager) to automatically get SSL certificates for our ingresses. I configure the certificate manager to use Lets Encrypt as certificate issuer.


## Installation

We use Helm 3 to install cert-manager:

```
$ kubectl create namespace cert-manager
$ helm repo add jetstack https://charts.jetstack.io
$ helm repo update
$ helm upgrade --install cert-manager jetstack/cert-manager --namespace cert-manager --version v1.7.1 --values helm-values.yaml
```


## Custom certificate authority for local home services

### Private key


This generates the `anton-johansson-home-services-ca.key`. This needs to be kept secret and is used to create the actual certificate that we need to trust.

### Certificate

```
$ openssl req -x509 -new -nodes -key anton-johansson-ca.key -sha256 -days 7300 -out anton-johansson-ca.pem -subj '/C=SE/CN=Anton Johansson Certificate Authority/O=Anton Johansson'
```

This generates the actual certificate that we need to trust.

### Signing new certificates

Use the private key and the certificate to create and sign new certificates. For now, we are using cert-manager to do this for us, but it can be done separately too.


### Issuers

Generate the intermediate certificate authority for home services:

```
$ openssl genrsa -out anton-johansson-home-services-ca.key 4096
$ openssl req -new \
    -subj "/C=SE/O=Anton Johansson/OU=Home/CN=Anton Johansson Home Services Intermediate CA" \
    -key anton-johansson-home-services-ca.key \
    -out anton-johansson-home-services-ca.csr
$ openssl x509 -req \
    -days 7300 \
    -extfile ./openssl.conf \
    -extensions intermediate_certificate_authority \
    -CAcreateserial \
    -CA ~/path/to/anton-johansson-ca.pem \
    -CAkey ~/path/to/anton-johansson-ca.key \
    -in anton-johansson-home-services-ca.csr \
    -out anton-johansson-home-services-ca.pem
```

Install the issuers by running the following:

```
$ kubectl create secret generic --namespace cert-manager anton-johansson-home-services-ca --from-file=tls.crt=./anton-johansson-home-services-ca.pem --from-file=tls.key=./anton-johansson-home-services-ca.key
$ kubectl apply -f issuers.yaml
```

I have the following cluster issuers:

* `letsencrypt`
* `letsencrypt-staging` (useful only for testing cert-manager upgrades and similar)
* `anton-johansson-home-services-ca` (local services)


## Using certificates

To use dynamic SSL certificates, you create `Certificate` resources. These resources will in turn generate `Secret` resources that you can use in your tls-configuration. Here is an example:

```yaml
---
kind: Certificate
apiVersion: cert-manager.io/v1
metadata:
  name: some-service
  namespace: test
spec:
  secretName: some-service-certificate
  commonName: some-external-domain.com
  dnsNames:
    - some-external-domain.com
  issuerRef:
    name: letsencrypt
    kind: ClusterIssuer
    group: cert-manager.io

---
kind: Ingress
apiVersion: networking.k8s.io/v1
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
            pathType: Prefix
            backend:
              service:
                name: some-service
                port:
                  number: 8080
  tls:
    - secretName: some-service-certificate
      hosts:
        - some-external-domain.com
```
