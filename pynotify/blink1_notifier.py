import time
from notifier import Notifier
from blink1.blink1 import Blink1


def blink_set_state(blink1,fade_millis,rgbstr,ledn=0):
        rgb=Blink1.parse_color_string( rgbstr )
        blink1.fade_to_rgbn( fade_millis, rgb[0],rgb[1],rgb[2], ledn)


class Blink1Notifier (Notifier):
    """Abstract class to implement notifier"""

    def __init__(self, state='unknown', alert_level=0,blinking=False):
        super(Blink1Notifier,self).__init__(state,alert_level,blinking)
        self.blink1=Blink1()
        if( self.blink1.dev == None ):
            raise UserWarning('No blink(1) devine found')

        self.fade_millis=300
        self.previous_state=None
        self.set_state(self.state)

    def unknown(self):
        self.state='unknown'
        blink_set_state(self.blink1, self.fade_millis, '#770000',1)
        blink_set_state(self.blink1, self.fade_millis, '#007700',2)

    def off(self):
        self.state='off'
        blink_set_state(self.blink1, self.fade_millis, '#000000')

    def ok(self):
        self.state='ok'
        blink_set_state(self.blink1, self.fade_millis, '#00FF00')

    def warning(self):
        self.state='warning'
        blink_set_state(self.blink1, self.fade_millis, '#FF5500')

    def critical(self):
        self.state='critical'
        blink_set_state(self.blink1, self.fade_millis, '#FF0000')

    def alert(self, level=0):
        for i in range(0,30):
            blink_set_state(self.blink1, self.fade_millis, '#FF0000',1)
            blink_set_state(self.blink1, self.fade_millis, '#0000FF',2)
            time.sleep( 0.25 )
            blink_set_state(self.blink1, self.fade_millis, '#0000FF',1)
            blink_set_state(self.blink1, self.fade_millis, '#FF0000',2)
            time.sleep( 0.25 )
        #
        #while [ 1 ] ; do
        #  blink1-tool -l 2 --red
        #  blink1-tool -l 1 --blue
        #  sleep 0.5
        #  blink1-tool -l 1 --red
        #  blink1-tool -l 2 --blue
        #  sleep 0.5
        #done

    def blink(self):
        raise NotImplementedError("Abstract")

    def unblink(self):
        raise NotImplementedError("Abstract")
