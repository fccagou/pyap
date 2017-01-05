import time
from pyap.notifier import Notifier
from blink1.blink1 import Blink1


def blink_set_state(blink1,fade_millis,rgbstr,ledn=0):
        rgb=Blink1.parse_color_string( rgbstr )
        blink1.fade_to_rgbn( fade_millis, rgb[0],rgb[1],rgb[2], ledn)


class Blink1Notifier (Notifier):
    """Abstract class to implement notifier"""

    # TODO: Actually, I haven't tried to manage more than one Blink(1) device.
    # So all Notifiers use the same device. It's possible to choose a different
    # led by notifier. So more then 2 Blink1Notifier as no sens.
    # The Notifier must change to allow more than one device.

    __single_blink_object=None

    def __init__(self, state='unknown', alert_level=0,blinking=False,
           led = 0,
           crit_color = '#FF0000',
           warn_color = '#FF5500',
           ok_color = '#00FF00',
           unknown_color = '#999999',
            ):

        super(Blink1Notifier,self).__init__(state,alert_level,blinking)

        if Blink1Notifier.__single_blink_object is None:
            Blink1Notifier.__single_blink_object = Blink1()

        self.blink1=Blink1Notifier.__single_blink_object
        if( self.blink1.dev == None ):
            raise UserWarning('No blink(1) devine found')

        self.fade_millis=300
        self.previous_state=None
        self.led = led

        self.crit_color = crit_color
        self.warn_color = warn_color
        self.ok_color = ok_color
        self.unknown_color = unknown_color
        self.set_state(self.state)

    def unknown(self):
        self.state='unknown'
        blink_set_state(self.blink1, self.fade_millis, self.unknown_color,self.led)

    def off(self):
        self.state='off'
        blink_set_state(self.blink1, self.fade_millis, '#000000')

    def ok(self):
        self.state='ok'
        blink_set_state(self.blink1, self.fade_millis, self.ok_color, self.led)

    def warning(self):
        self.state='warning'
        blink_set_state(self.blink1, self.fade_millis, self.warn_color, self.led)

    def critical(self):
        self.state='critical'
        blink_set_state(self.blink1, self.fade_millis, self.crit_color, self.led)

    def alert(self, level=0):
        for i in range(0,30):
            blink_set_state(self.blink1, self.fade_millis, '#FF0000',1)
            blink_set_state(self.blink1, self.fade_millis, '#0000FF',2)
            time.sleep( 0.25 )
            blink_set_state(self.blink1, self.fade_millis, '#0000FF',1)
            blink_set_state(self.blink1, self.fade_millis, '#FF0000',2)
            time.sleep( 0.25 )

    def blink(self):
        raise NotImplementedError("Abstract")

    def unblink(self):
        raise NotImplementedError("Abstract")
