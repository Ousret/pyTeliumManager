import os, pty
import curses.ascii
import threading
from faker import Faker
from telium.constant import *
from telium.payment import TeliumData, TeliumAsk, TeliumResponse


class FakeTeliumDevice:

    def __init__(self):
        self._master, self._slave = pty.openpty()
        self._s_name = os.ttyname(self._slave)

        self._fake = Faker()

        self._fake_device = threading.Thread(target=self.__run)
        self._fake_device.start()

    @property
    def s_name(self):
        return self._s_name

    @staticmethod
    def _has_signal(data, signal):
        return data[0] == curses.ascii.controlnames.index(signal)

    @staticmethod
    def _create_signal(signal):
        return bytes([curses.ascii.controlnames.index(signal)])

    def _wait_signal(self, signal):
        return FakeTeliumDevice._has_signal(os.read(self._master, 1), signal)

    def _send_signal(self, signal):
        os.write(self._master, FakeTeliumDevice._create_signal(signal))

    def __run(self):

        if self._wait_signal('ENQ'):

            self._send_signal('ACK')

            raw_data = os.read(self._master, TERMINAL_ANSWER_COMPLETE_SIZE)

            if TeliumData.lrc_check(raw_data) is True:

                payment_pending = TeliumAsk.decode(raw_data)

                print('from master : ', payment_pending.__dict__)

                self._send_signal('ACK')  # Accept data from master

                if not self._wait_signal('EOT'):
                    self._send_signal('NAK')
                    exit(1)

                # print(self._fake.credit_card_number(card_type=None))

                my_response = TeliumResponse(
                    payment_pending.pos_number,
                    TERMINAL_PAYMENT_SUCCESS,
                    payment_pending.amount,
                    payment_pending.payment_mode,
                    (self._fake.credit_card_number(card_type='visa16') + '0' * 39),
                    payment_pending.currency_numeric,
                    '0' * 10
                )

                self._send_signal('ENQ')

                if self._wait_signal('ACK'):
                    print('response len = ', len(my_response.encode()))
                    print('')
                    os.write(self._master, bytes(my_response.encode(), 'ascii'))

                    if self._wait_signal('ACK'):
                        self._send_signal('EOT')
                        exit(0)

                    self._send_signal('NAK')

                else:

                    self._send_signal('NAK')
                    exit(1)

            else:
                self._send_signal('NAK')
                exit(1)
