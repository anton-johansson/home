# Home configuration

[![Build Status](https://travis-ci.org/anton-johansson/home.svg?branch=master)](https://travis-ci.org/anton-johansson/home)

The configuration for my home tools, such as Home Assistant.


## Installing Kubernetes

The Home configuration is running on a single-host Kubernetes cluster. First, we need to disable swap on the machine. This can be done with `swapoff -a`, but this won't be persisted, so also comment out the swap row in `/etc/fstab`. We also need to register two virtual IPs for our server (one for internal HTTP traffic and one for external HTTP traffic). Do this by modifying `/etc/network/interfaces` and add them, something like this:

```
auto <interface>:1
iface <interface>:1 inet static
address         <virtual IP 1>
netmask         255.255.255.0
broadcast       <broadcast>

auto <interface>:2
iface <interface>:2 inet static
address         <virtual IP 2>
netmask         255.255.255.0
broadcast       <broadcast>
```

Then, to install the cluster, the following is done:

```shell
$ git clone git@github.com:anton-johansson/home.git ~/projects/
$ git clone git@github.com:amimof/kubernetes-the-right-way.git ~/projects/
$ ansible-playbook --ask-become-password --inventory ~/projects/home/ktrw-inventory ~/projects/kubernetes-the-right-way/install.yml
```


## Preparing

Some files needs to be created in order for everything to run properly.

```shell
echo "<redacted>" | tee /home/$USER/home/home-assistant/bearer-token
```

## Running home tools

```shell
$ docker-compose start
```
