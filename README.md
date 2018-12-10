# Home configuration

[![Build Status](https://travis-ci.org/anton-johansson/home.svg?branch=master)](https://travis-ci.org/anton-johansson/home)

The configuration for my home tools, such as Home Assistant.


## Preparing

Some files needs to be created in order for everything to run properly.

```shell
echo "<redacted>" | tee /home/$USER/home/home-assistant/bearer-token
```

## Running home tools

```shell
$ docker-compose start
```
