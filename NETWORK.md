# Network configuration

I'm using a Google WiFi mesh network setup.


## Reserved IP addresses

| IP suffix       | Device                                     | Hostname        |
| --------------- | ------------------------------------------ | --------------- |
|            `.1` | Gateway                                    |
|   `.2` -   `.9` | Reserved for network related devices*      |
|           `.10` | Home server                                | `home-server`   |
|           `.11` | Desktop                                    | `anton-desktop` |
|           `.12` | Laptop                                     | `anton-laptop`  |
|           `.13` | Cellphone                                  | `anton-phone`   |
|           `.14` | Chromecast                                 |
|           `.15` | TV                                         |
|           `.16` | Sonos PLAYBAR                              | `sonos-playbar` |
|           `.17` | Sonos ONE (Kitchen)                        | `sonos-kitchen` |
|           `.18` | Nintendo Switch                            |
|           `.19` | Sonos ONE (Bedroom)                        | `sonos-bedroom` |
|  `.20` -  `.79` | Reserved for additional internal devices   |
|           `.80` | NGINX for internal traffic                 |
|           `.81` | NGINX for external traffic                 |
|  `.82` -  `.99` | Reserved for services hosted in Kubernetes |
| `.100` - `.254` | Common DHCP pool                           |

\* These can be smart switches or additional WiFi points. Currently, my additional WiFi points cannot have static IP addresses, so they're using the regular DHCP pool, but if that ever changes, they'll be moved to this reservation.


## Port forwarding

| Protocol | External port | Internal port | IP suffix |
| -------- | ------------- | ------------- | --------- |
| SSH      |         `22`  |          `22` |     `.10` |
| HTTP     |         `80`  |          `80` |     `.10` |
| HTTPS    |         `443` |         `443` |     `.10` |
| Factorio |       `34197` |       `32407` |     `.10` |
