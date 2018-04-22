# Philips TV pairing utility

This utility contains a python3 script that handles the pairing of a Philips TV and outputs the generated username and password.


## Requirements

To run this, you need Python3, with additional packages installed as follows:
```sh
pip3 install pycrypto
```


## Usage

```python
python3 pair.py 192.168.1.123
```

Successful output:
```
Username: abc123
Password: abcdefghij1234567890
```

Another utility that was used for testing is powering the TV on or off, using this script:
```python
python3 power.py --username anton --password test 192.168.1.123
```


## Resources and inspiration

* [Home Assistant forum thread](https://community.home-assistant.io/t/philips-android-tv-component/17749/34)
* [GitHub repository](https://github.com/suborb/philips_android_tv)
* [GitHub repository](https://github.com/mveken/home_assistant)
