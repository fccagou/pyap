


class Notifier (object):
    """Abstract class to implement notifier"""

    def __init__(self, state='off', alert_level=0,blinking=False):
        super(Notifier,self).__init__()
        self.state=state
        self.alert_level=alert_level
        self.blinking=blinking

    def set_state(self,state):
        prev_state=self.state
        try:
            getattr(self,state)()
        except:
            self.state=prev_state
            raise NotImplementedError("Unknown state '%s' " % state)


    def off(self):
        raise NotImplementedError("Abstract")

    def ok(self):
        raise NotImplementedError("Abstract")

    def warning(self):
        raise NotImplementedError("Abstract")

    def critical(self):
        raise NotImplementedError("Abstract")

    def alert(self, level):
        raise NotImplementedError("Abstract")

    def blink(self):
        raise NotImplementedError("Abstract")

    def unblink(self):
        raise NotImplementedError("Abstract")
