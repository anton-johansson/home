# Home configuration

The configuration for my home tools, such as Home Assistant.


## Installing Kubernetes

The Home configuration is running on a single-host Kubernetes cluster. First, we need to disable swap on the machine. This can be done with `swapoff -a`, but this won't be persisted, so also comment out the swap row in `/etc/fstab`.

Then, to install the cluster, the following is done:

```shell
$ git clone git@github.com:anton-johansson/home.git ~/projects/
$ git clone git@github.com:amimof/kubernetes-the-right-way.git ~/projects/
$ ansible-playbook --ask-become-password --inventory ~/projects/home/ktrw-inventory ~/projects/kubernetes-the-right-way/install.yml
```
