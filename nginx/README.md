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


## Accessing deCONZ

The deCONZ instance is exposed through nginx because it's hidden within the Docker network, but there is no domain configured for it. Route `deconz.anton-johansson.com` to the home server through the `hosts` file in order to access deCONZ.
