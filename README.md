# Home configuration

[![Build Status](https://travis-ci.org/anton-johansson/home-assistant-config.svg?branch=master)](https://travis-ci.org/anton-johansson/home-assistant-config)

The configuration for my home tools, such as Home Assistant.


## Running home tools

```shell
$ docker-compose start
```


## Checking Home Assistant configuration

```shell
$ docker exec -it home-assistant python -m homeassistant --config /config --script check_config
```
