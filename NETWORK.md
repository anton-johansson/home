# Network configuration

I'm using a Google WiFi mesh network setup.


## Reserved IP addresses

| IP suffix       | Device                                     | Hostname        |
| --------------- | ------------------------------------------ | --------------- |
| `.  1`          | Gateway                                    |
| `.  1` - `.  9` | Reserved for network related devices*      |
| `. 10`          | Home server                                | `home-server`   |
| `. 11`          | Desktop                                    | `anton-desktop` |
| `. 12`          | Laptop                                     | `anton-laptop`  |
| `. 13`          | Cellphone                                  | `anton-phone`   |
| `. 14`          | Chromecast                                 |
| `. 15`          | TV                                         |
| `. 16`          | Sonos PLAYBAR                              |
| `. 17`          | Sonos ONE (Kitchen)                        |
| `. 18`          | Nintendo Switch                            |
| `. 19`          | Sonos ONE (Bedroom)                        |
| `. 20` - `. 79` | Reserved for additional internal devices   |
| `. 80`          | Internal NGINX                             |
| `. 81`          | External NGINX                             |
| `. 82` - `. 99` | Reserved for services hosted in Kubernetes |
| `.100` - `.254` | Common DHCP pool                           |

\* These can be smart switches or additional WiFi points. Currently, my additional WiFi points cannot have static IP addresses, so they're using the regular DHCP pool, but if that ever changes, they'll be moved to this reservation.


## Port forwarding

| Protocol | Port  | IP suffix |
| -------- | ----- | --------- |
| SSH      | `22`  | `. 10`    |
| HTTP     | `80`  | `. 10`    |
| HTTPS    | `443` | `. 10`    |
