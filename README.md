# pynotif

Notification using python

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

The file [pyserialnotif](pyserialnotif) is an example.

The tests are made on this hardware

![Db9 test hardware](images/pyserialnotify_hw_test.png)


## TODO

- use log instead of print in Db9
- make tests case
- make a notification factory that use Db9
- implement other notification type
- make server listening for incomming notification (json, yaml, ?? /  http,https)
- incomming plugins for various sources: 

  - alerte with dif levels: nagios, shinken ...
  - incomming mail: thunderbid, mutt, fetchmail,  ...

