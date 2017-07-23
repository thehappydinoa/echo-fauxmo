# echo-fauxmo

For controlling local devices with the Amazon Echo. And for controlling iTach devices to send ir signals to devices. This replaces the Harmony Hub
Originally Based on [echo](https://github.com/toddmedema/echo)

## Quick Start

1. `git clone *this_repo*`
2. `cd *this_repo*`
3. `pip install -r requirements.txt`
4. `python example-minimal.py`
5. Tell Echo, "discover my devices"
6. Use Echo's "turn off device" and "device on" to see True/False script output

## Working with iTach

1. Find the IR codes that you want to send with [iLearn from Global Cache](https://www.globalcache.com/files/software/iLearn.exe)
2. Edit 'itach-device-handler.py' with the IPs and IR codes you want to use
3. `python itach-device-handler.py`

## Working with XBox

1. To find the IP of your Xbox, go to Settings -> Network -> Advanced settings. To find your Live device ID, go to Settings -> System -> Console info. NOTE: It's probably a good idea to keep this information a secret!
2. Edit 'wol-device-handler.py' to include your XBox Live ID and IP

## Optional

* I would suggest using `Screen` to make it headless
Install `Screen` by running

```
sudo apt-get install screen
```

## TODO

* Make Web Server for if-then statements (like a more customizable version of IFTTT)
* Make Raspberry Pi OS with Web Server for instant deployment

## FAQ

### Error Messages
*`ImportError: No module named setuptools` 
    1. Download [ez_setup.py](https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py)
    2. `sudo python ez_setup.py`


## Resources

* [Fauxmo](https://github.com/makermusings/fauxmo)
* [Echo](https://github.com/toddmedema/echo)
* [AQUOS-Remote-Python](https://github.com/thehappydinoa/AQUOS-Remote-Python)
* [iTach Downloads and Docs](https://www.globalcache.com/downloads/)
* [Screen How-to](https://www.rackaid.com/blog/linux-screen-tutorial-and-how-to/)
* [Run Screen Detached on startup](https://coderwall.com/p/quflrg/run-a-script-on-startup-in-a-detached-screen-on-a-raspberry-pi)

## DEPENDENCIES

This has been tested with Python 2.6 and 2.7.

## LICENSE

MIT License
