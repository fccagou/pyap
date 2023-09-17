# pyap (PYthon Alert Processor  / P....n Y'A Personne)

Pyap is a little tools used to process alert sent by differents ways.

_Previously named pynotif, I need to rename it because of conflicted
naming with python-notify from libnotify._


1. [History](# history)
2. [Serial Db9](#serial-db9)
3. [pyap](#pyap)
4. [http poller](#http-poller)
5. [Nagios/Shinken http poller](#nagios/shinken-http-poller)
6. [blink(1)](#blink(1))
7. [Container](#container)
8. [TODO](#todo)
9. [Changelog](#changelog)
   * [[v0.6.0] - 2023-09-17](#[v0.6.0]---2023-09-17)


## History

I would like to get physical notifications to be informed when a new event
occurs on my computer.

I would like a solution with less electronic as possible.


Many solutions exist :

- using an [arduino](https://www.arduino.cc/en/Main/arduinoBoardNano)
- using commercial solutions like [blink(1)](http://blink1.thingm.com/)
- or DIY solution

I've chosen DIY solution and begun begun with hardware I have in my cupboard,
a USB/Serial cable.

I create the first python class [Db9](#Serial Db9)

## Serial Db9

Inspired by a linuxfocus article on [sled](http://linuxfocus.org/English/January2001/article186.shtml)
the Db9 class use ioctl to switch on/off the output pins.

The file [pyap-serial](tests/pyap-serial) is an example.


The tests are made on this hardware

- pin5 is the Ground
- pin4 is the green led for ok status
- pin7 is the red led for critical status
- pin3 is unusable this way.
- Two 1k resistors protect each led


![Db9 test hardware](images/pyserialnotify_hw_test.png)



Just test using `python tests/pyap-serial <tty>`

## pyap

Because serial port must be opened to keep the light on, I had to create a
program that controls the lights and receives change orders.

[Pyap](pyap) is a server listening for http requests and poll remote status
through http requests to switch leds on/off.

Replace __PWD__ in tests/tests.conf according to your path and run the server:

By default, pyap is running as daemon mode and writes his pid in /var/run/pyap.pid file.
For tesing or debugging, use --nopid and --fg parameters.

```
$ export PYTHONPATH=$(pwd); bin/pyap --nopid --fg -v --server --conf=tests/test.conf
[+] -  Using config file tests/test.conf
[+] -  Blink(1) found
[!] -  serial_led not found
[+] -  Running http poller
[i] -  [+] Get status from file:///home/pi/src/pyap/tests/status/n1
[+] -  Serving HTTP on port 8080...
[i] -  poller status ( {"services":{ "ok":1, "warn":0, "crit":0, "unknown":0}} )
[i] -  [+] Get status from file:///home/pi/src/pyap/tests/status/n2
[i] -  poller status ( {"services":{ "ok":0, "warn":0, "crit":0, "unknown":0}} )
[i] -  Global status ( {'crit': 0, 'warn': 0, 'ok': 1, 'unknown': 0} )
^C[+] -  End asked by user...bye bye !
[+] -  Waiting end of process
```

Test the commands:

```
curl http://127.0.0.1:8080/alert/ok
curl http://127.0.0.1:8080/alert/warning
curl http://127.0.0.1:8080/alert/critical
curl http://127.0.0.1:8080/alert/ack

curl http://127.0.0.1:8080/alert/security
curl http://127.0.0.1:8080/alert/security/ack

curl http://127.0.0.1:8080/alert/christmas
curl http://127.0.0.1:8080/alert/christmas/ack
```


## http poller

Actually `http poller` is a thread in `pyap` as a test code. It must be coded
in it own program. Pyap must not do polling AND sending alerts.

If urls are provided in conf file or in parameters, a thread is started to
poll informations from all the url. Request must returns json
values of services status in the form :
```
{"services":{ "ok":123, "warn":1, "crit":0, "unknown":0}}
```

## Nagios/Shinken http poller

The `data/nagios2json.php` file can be used on nagios/shinken server as a http
poller. The php code uses [mklivestatus](http://mathias-kettner.de/checkmk_livestatus.html).

## blink(1)

[blink(1)](http://blink1.thingm.com/) led device is now usable. see file `blink1-python-update.sh`
Copy `data/51-blink1.rules` to `/etc/udev/rules.d` to allow all users access to
the device.

## Container

Actually, the Dockefile is used to build rpm package and an image
based on almalinux.

To build all, just run

    podman build --tag pyap .

To test the image, you need to get the device path.
With lsusb, get bus and device values and the path is
`/dev/bus/usb/<BUS-NUMBER>/<DEV-NUMBER>`

Example:

    $ lsusb | grep blink
    Bus 001 Device 008: ID 27b8:01ed ThingM blink(1)
        ^^^        ^^^

    Device path is /dev/bus/usb/001/008

Then run a test that must switch on the blink(1) and allow web access on
`localhost:8080`:


    ( DEVICEPATH="$( lsusb | grep blink | cut -d: -f1 | awk '{ print "/dev/bus/usb/"$2"/"$4 }' )"; \
    podman run --rm -ti -p 8080:8080 --device="$DEVICEPATH" pyap )



## TODO

See [TODO.md](https://github.com/fccagou/pyap/blob/master/TODO.md)

## Changelog

### [v0.6.0] - 2023-09-17

- Add python3 support
- Add container support
- Depreciate python2
- Depreciate rhel 6 release
