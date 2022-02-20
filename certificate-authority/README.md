# Certificate authority

I have my own certificate authority, used to sign new certificate requests for services.


## Private key

```
$ openssl genrsa -aes128 -out anton-johansson-ca.key 4096
```

This generates the `anton-johansson-ca.key`. This needs to be kept secret and is used to create the actual certificate that we need to trust.

## Certificate

```
$ openssl req -x509 -new -nodes -key anton-johansson-ca.key -sha256 -days 7300 -out anton-johansson-ca.pem -subj '/C=SE/CN=Anton Johansson Certificate Authority/O=Anton Johansson'
```

This generates the actual certificate that we need to trust.
