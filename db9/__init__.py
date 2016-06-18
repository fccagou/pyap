
import struct
import termios
import fcntl


class Db9(object):

    PIN1 = termios.TIOCM_CD
    PIN2 = termios.TIOCM_SR
    PIN3 = termios.TIOCM_ST
    PIN4 = termios.TIOCM_DTR
    PIN5 = -1
    PIN6 = termios.TIOCM_DSR
    PIN7 = termios.TIOCM_RTS
    PIN8 = termios.TIOCM_CTS
    PIN9 = termios.TIOCM_RI

    ALL_OUTPUT = PIN3 | PIN4 | PIN7

    __tty = None
    __state = ' ' * 8
    __fd = None
    __pins = (ALL_OUTPUT, PIN1, PIN2, PIN3, PIN4, PIN5, PIN6, PIN7, PIN8, PIN9)

    def __init__(self, tty):
        self.__tty = tty

    def connect(self):
        self.__fd = open(self.__tty, 'w+')
        self.__state = fcntl.ioctl(
            self.__fd, termios.TIOCMGET, '\000\000\000\000\000\000\000\000')

    def switch_on(self, pin):
        self.__state = fcntl.ioctl(self.__fd, termios.TIOCMSET, struct.pack(
            'l', struct.unpack('l', self.__state)[0] | pin))

    def switch_off(self, pin):
        self.__state = fcntl.ioctl(self.__fd, termios.TIOCMSET, struct.pack(
            'l', struct.unpack('l', self.__state)[0] & ~pin))

    def is_on(self,pin):
        return ((struct.unpack('l',self.__state)[0] & pin) == pin)

    def disconnect(self):
        self.__fd.close()

    def write(self, datas):
        self.__fd.write(datas)
