import time
from pynotify.notifier import Notifier
from db9 import Db9


def blink_set_state(blink1,fade_millis,rgbstr,ledn=0):
        rgb=Blink1.parse_color_string( rgbstr )
        blink1.fade_to_rgbn( fade_millis, rgb[0],rgb[1],rgb[2], ledn)


class SerialLedNotifier (Notifier):
    OK_LED = Db9.PIN4
    CRITICAL_LED = Db9.PIN7

    def __init__(self, tty, state='unknown', alert_level=0,blinking=False):
        super(SerialLedNotifier,self).__init__(state,alert_level,blinking)
        self.serial_output=Db9(tty)
        self.serial_output.connect()

        self.fade_millis=300
        self.previous_state=None
        self.set_state(self.state)

    def __del__(self):
        if self.serial_output is not None:
            self.serial_output.disconnect()

    def unknown(self):
        self.state='unknown'
        raise NotImplementedError("Abstract")

    def off(self):
        self.state='off'
        self.serial_output.switch_off(Db9.ALL_OUTPUT)

    def ok(self):
        self.state='ok'
        self.serial_output.switch_off(Db9.ALL_OUTPUT)
        self.serial_output.switch_on(SerialLedNotifier.OK_LED)

    def warning(self):
        self.state='warning'
        self.serial_output.switch_on(SerialLedNotifier.OK_LED)
        self.serial_output.switch_on(SerialLedNotifier.CRITICAL_LED)

    def critical(self):
        self.state='critical'
        self.serial_output.switch_off(Db9.ALL_OUTPUT)
        self.serial_output.switch_on(SerialLedNotifier.CRITICAL_LED)

    def alert(self, level=0):
        raise NotImplementedError("Abstract")

    def blink(self):
        raise NotImplementedError("Abstract")

    def unblink(self):
        raise NotImplementedError("Abstract")

