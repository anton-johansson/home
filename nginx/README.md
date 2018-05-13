# nginx

Provides configuration for the `nginx` container.


## Renew SSL certificates

```sh
$ sudo docker run -it --rm \
      --volume /home/anton/home/nginx/certificates:/etc/letsencrypt \
      --volume /home/anton/home/nginx/letsencrypt:/data/letsencrypt \
      certbot/certbot \
      certonly \
      --webroot --webroot-path=/data/letsencrypt \
      -d home.anton-johansson.com
```


## SSL for Arduino clients

The Arduino units have a limited set of SSL ciphers available, and therefore any HTTPS receivers that expects communications from Arduino units require any of the following ciphers present:

* `AES128-SHA`
* `AES256-SHA`

More information can be found [here](http://wiki.sitebuilt.net/index.php?title=Esp8266).
