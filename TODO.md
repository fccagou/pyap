*********
TODO LIST
*********


Packaging
=========

- make deb packaging

Development
===========

- make tests case
- make a choise to manage pyusb/blink1 source code. Use git module ?

Refactoring
===========

- bin/pyap is a quick and dirty code for tests. The code must be refactored.
- have a thread to manage led states doing on/off
- Use msgQ or something else to send new states to led state manager

Notifiers
=========

Blink1Notifier
--------------

Actually, I haven't tried to manage more than one Blink(1) device.
So all Notifiers use the same device. It's possible to choose a different
led by notifier. So more than 2 Blink1Notifier as no sens.
The Notifier must change to allow more than one device.


Features
========

- add syslog info for daemon mode

- Serve web status page

  Set Color according to notifier color
  Update colorscheme in conf file

- implement blink and alert API.
  /!\ - security access to web access.

- add other notification types
- incoming `pollers` for various sources

  - alerts with different levels: nagios, shinken ...
  - incomming mail: thunderbid, mutt, fetchmail,  ...


```


                               (client1) (clientx)
                                   |        |
                                   |        |
                                   |        |
                                   V        V
 <----- (poller 1) ----------->  +-----------+ --------> notif type 1 <
 <-----     .                    |           |                .
 <-----     .              --->  |    pyap   | ---->          .
 <-----     .                    |           |                .
 <----- (poller x) ----------->  +-----------+ --------> notif type n <


```


DONE
====
- add conf file using json to set notifiers and urls.
- add better logging.
- add daemon mode
- add init/systemd service for rpm system.
- associate a notifier to an url.
- Serve web status page

  If you only use 1 Led, the led color indicates the more critical status from
  all the systems checked so you don't know which one is critical or not.
  To have more details, pyap should serve a web page showing status for
  each system checked.

  It could be usefull to associate an alias to display for eah system checked and,

```
    Icescreams dispenser :  (ok:  12)  (warn: 1)  (Unknown: 0) (crit: 0)
    Subnet X             :  (ok: 254)  (warn: 2)  (Unknown: 0) (crit: 0)
    IDS Alertes          :  (ok: 123)  (warn: 0)  (Unknown: 0) (crit: 1)

```
