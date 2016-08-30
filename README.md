# pyap (PYthon Alert Processor  / P....n Y'A Personne)

Pyap is a little tools used to process alert sent by differents ways.

_Previously named pynotif, I need to rename it because of conflicted
naming with python-notify from libnotify._

## History

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

[Pyap](pyap) is a server listening for http requests to switch leds on/off.

Run the server:
```
$ (export PYTHONPATH=$(pwd):${PYTHONPATH}; python bin/pyap -v --tty /dev/ttyXXX file://$(pwd)/tests/status/n1 file://$(pwd)/tests/status/n2 )
[+] - Running nagios poller
[+] - Serving HTTP on port 8080...
```

Test the commands:

```
curl http://127.0.0.1:8080/alert/ok
curl http://127.0.0.1:8080/alert/warning
curl http://127.0.0.1:8080/alert/critical
curl http://127.0.0.1:8080/alert/ack

curl http://127.0.0.1:8080/alert/security
curl http://127.0.0.1:8080/alert/security/ack
```


## nagios poller

Actually `nagios_poller` is a thread in `pyap` as a test code. It must be coded
in it own program. Pyap must not do polling AND sending alerts.

If the optional pyap param (`nagios_url_status`) is set, a thread is started to
poll informations from the url nagios_url_status. Request must returns json values
of nagios services status in the form :
```
{"services":{ "ok":123, "warn":1, "crit":0, "unknown":0}}
```

## blink(1)

Blink(1) led is now usable. see file `blink1-python-update.sh`

## TODO

- make deb packaging
- make a choise to manage pyusb/blink1 source code. Use git module ?
- make tests case
- other notification types
- incoming `pollers` for various sources

  - alerte with dif levels: nagios, shinken ...
  - incomming mail: thunderbid, mutt, fetchmail,  ...



```


                               (client1) (clientx)
                                   |        |
                                   |        |
                                   |        |
                                   V        V
 <----- (poller 1) ----------->  +-----------+ --------> notif type 1 <
 <-----     .                    |           |                .
 <-----     .              --->  |  pyap  | ---->          .
 <-----     .                    |           |                .
 <----- (poller x) ----------->  +-----------+ --------> notif type n <


```
