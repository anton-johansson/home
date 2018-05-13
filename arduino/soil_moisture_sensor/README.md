# Soil moisture sensor

Provides a unit that checks the moisture in the soil for plants. Useful for reminders to water the plants.


## Components

| Component | Image | Function |
| --------- | ----- | -------- |
| [Wemos D1 mini](https://www.m.nu/esp8266/d1-mini-v30) | ![Wemos D1 mini](https://images.m.nu/data/product/1076f860/wemos_d1_mini_v30_1.jpg) | The Arduino board itself. |
| [Soil moisture sensor](https://www.kjell.com/se/sortiment/el-verktyg/arduino/moduler/luxorparts-jordfuktsmatare-for-arduino-p87941) | ![Soil moisture sensor](https://www.kjell.com/se/image/Product_242997sv/full/1/luxorparts-jordfuktsmatare-for-arduino) | The sensor component. |


## Code notes

### Enforcing data to be sent over HTTP

When sending data over HTTP, the only way to enforce it to actually be sent is to read something from the response. Reading the entire response body (`client.readString()`) seems to be an expensive operation, and takes a few seconds to perform. Therefore, it's useful to read to the first line separator (`client.readStringUntil('\n');`). This also provides useful information, so we easily can see whether or not the call succeeded (`200 OK`).
