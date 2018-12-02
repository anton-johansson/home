# Home configuration

[![Build Status](https://travis-ci.org/anton-johansson/home.svg?branch=master)](https://travis-ci.org/anton-johansson/home)

The configuration for my home tools, such as Home Assistant.


## Preparing

Environment variables needs to be set up before starting the services.

```shell
echo "HOST_IP=$(hostname -I | cut -d ' ' -f1)" | sudo tee -a /etc/environment
```

## Running home tools

```shell
$ docker-compose start
```
