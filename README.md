# Home Assistant configuration

[![Build Status](https://travis-ci.org/anton-johansson/home-assistant-config.svg?branch=master)](https://travis-ci.org/anton-johansson/home-assistant-config)

The configuration for my Home Assistant.


## Running Home Assistant

```shell
$ docker-compose start
```


## Checking configuration

```shell
$ docker exec -it home-assistant python -m homeassistant --config /config --script check_config
```
