import os, pty
import curses.ascii
import threading
from telium.constant import *
from telium.payment import TeliumAsk, TeliumResponse
from hexdump import hexdump


class FakeTeliumDevice:

    def __init__(self):
        self._master, self._slave = pty.openpty()
        self._s_name = os.ttyname(self._slave)

        self._running = True

        self._fake_device = threading.Thread(target=self.__run)
        self._fake_device.start()

    def stop(self):
        self._running = False

    @property
    def s_name(self):
        return self._s_name

    @staticmethod
    def _has_signal(data, signal):
        if data[0] == curses.ascii.controlnames.index(signal):
            return True
        return False

    @staticmethod
    def _create_signal(signal):
        return bytes([curses.ascii.controlnames.index(signal)])

    def __run(self):

        while self._running:
            one_byte_signal = os.read(self._master, 1)

            #  Case of slave initiating communication
            if FakeTeliumDevice._has_signal(one_byte_signal, 'ENQ'):

                #  Notify slave that we're ready to receive data
                os.write(self._master, FakeTeliumDevice._create_signal('ACK'))

                data = os.read(self._master, TERMINAL_ANSWER_COMPLETE_SIZE)

                hexdump(data[1:-2])
                payment_pending = TeliumAsk.decode(str(data[1:-2], 'ascii'))

                print(payment_pending.__dict__)

                os.write(self._master, FakeTeliumDevice._create_signal('ACK'))

                one_byte_signal = os.read(self._master, 1)

                hexdump(one_byte_signal)

                #  Respond here..
            else:

                os.write(self._master, FakeTeliumDevice._create_signal('NAK'))


            hexdump(one_byte_signal)