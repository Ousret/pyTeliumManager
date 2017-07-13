from serial import Serial
from glob import glob
import curses.ascii
from telium.constant import *
from telium.payment import TeliumResponse


class SignalDoesNotExistException(KeyError):
    pass


class DataFormatUnsupportedException(Exception):
    pass


class TerminalInitializationFailedException(Exception):
    pass


class TerminalUnrecognizedConstantException(Exception):
    pass


class TerminalUnexpectedAnswerException(Exception):
    pass


class Telium:
    def __init__(self, path='/dev/ttyACM0', baudrate=9600, timeout=1):
        """
        Create Telium device instance
        :param path: str Path to serial emulated device
        :param baud: int Set baud rate
        :param timeout: int Maximum delai before hanging out.
        """
        self._path = path
        self._baud = baudrate
        self._device = Serial(self._path, self._baud, timeout=timeout)

    @staticmethod
    def get():
        """
        Auto-create a new instance of Telium. The device path will be infered based on most commom location.
        This won't be reliable if you have more than one emulated serial device plugged-in. Won't work either on NT plateform.
        :return: Fresh new Telium instance or None
        :rtype: telium.Telium
        """
        for path in TERMINAL_PROBABLES_PATH:
            probables = glob('%s*' % ''.join(filter(lambda c: not c.isdigit(), path)))
            if len(probables) == 1:
                return Telium(probables[0])
        return None

    def __del__(self):
        if self._device.is_open:
            self._device.close()

    @property
    def timeout(self):
        """
        Get current timeout value from pySerial device instance
        :return: Current timeout setting from device handled by pySerial
        :rtype: float
        """
        return self._device.timeout

    @property
    def is_open(self):
        """
        Verify whenever the device is actually opened or not via pySerial main instance.
        :return: True if still opened.
        :rtype: bool
        """
        return self._device.is_open

    def close(self):
        """
        Close the device if not already closed
        :return: True if device succesfuly closed
        :rtype: bool
        """
        if self._device.is_open:
            self._device.close()
            return True
        return False

    def open(self):
        """
        Open the device if not already opened
        :return: True if device succesfuly opened
        :rtype: bool
        """
        if not self._device.is_open:
            self._device.open()
            return True
        return False

    def _send_signal(self, signal):
        """
        Send single signal to device like 'ACK', 'NAK', 'EOT', etc.. .
        :param signal: str
        :return: True if signal was written to device
        :rtype: bool
        """
        if signal not in curses.ascii.controlnames:
            raise SignalDoesNotExistException("Le signal '%s' n'existe pas." % signal)
        return self._send(chr(curses.ascii.controlnames.index(signal))) == 1

    def _wait_signal(self, signal):
        """
        Read one byte from serial device and compare to expected.
        :param signal: str
        :return: True if received signal match
        :rtype: bool
        """
        one_byte_read = self._device.read(1)
        expected_char = curses.ascii.controlnames.index(signal)
        #  print('DEBUG wait_signal_received = ', curses.ascii.controlnames[one_byte_read[0]])

        return one_byte_read == expected_char.to_bytes(1, byteorder='big')

    def _send(self, data):
        """
        Send data to terminal
        :param data: str string representation to convert and send
        :return: Lenght of data actually sended
        :rtype: int
        """
        if not isinstance(data, str):
            raise DataFormatUnsupportedException("You should pass string to _send method, we'll convert it for you.")
        return self._device.write(bytes(data, TERMINAL_DATA_ENCODING))

    def _read_answer(self, expected_size=TERMINAL_ANSWER_COMPLETE_SIZE):
        """
        Download raw answer and convert it to TeliumResponse
        :return: TeliumResponse
        :raise: TerminalUnexpectedAnswerException If data cannot be converted into telium.TeliumResponse
        :rtype: telium.TeliumResponse
        """
        msg = self._device.read(size=expected_size)
        msg_len = len(msg)

        if msg_len != expected_size:
            raise TerminalUnexpectedAnswerException('Raw read expect size = {0} '
                                                    'but actual size = {1}.'.format(expected_size, msg_len))

        if msg[0] != curses.ascii.controlnames.index('STX'):
            raise TerminalUnexpectedAnswerException(
                'The first byte of the answer from terminal should be STX.. Have %s and except %s' % (
                    msg[0], curses.ascii.controlnames.index('STX').to_bytes(1, byteorder='big')))
        if msg[-2] != curses.ascii.controlnames.index('ETX'):
            raise TerminalUnexpectedAnswerException(
                'The byte before final of the answer from terminal should be ETX')

        return TeliumResponse.decode(msg)

    def _get_pending(self):
        """
        Method keeped for tests purposes, shouldn't use in fiable production environnement.
        Very slow computer performance can cause app to not catch data in time
        """
        self._device.timeout = 0.3
        self._device.read(size=1)
        self._device.timeout = 1

    def ask(self, telium_ask, raspberry=False):
        """
        Initialize payment to terminal
        :param telium.TeliumAsk telium_ask: Payment info
        :param bool raspberry: Set it to True if you'r running Raspberry PI
        :return: True if device has accepted to begin a new transaction.
        :rtype: bool
        """
        if raspberry:
            self._get_pending()

        # Send ENQ and wait for ACK
        self._send_signal('ENQ')

        if not self._wait_signal('ACK'):
            raise TerminalInitializationFailedException(
                "Payment terminal isn't ready to accept data from host. "
                "Check if terminal is properly configured or not busy.")

        # Send transformed TeliumAsk packet to device
        self._send(telium_ask.encode())

        # Verify if device has received everything
        if not self._wait_signal('ACK'):
            self._send_signal('EOT')
            return False

        # End this communication
        self._send_signal('EOT')

        return True

    def verify(self, telium_ask):
        """
        Wait for answer and convert it for you.
        :param telium.TeliumAsk telium_ask: Payment info
        :return: TeliumResponse, None or Exception
        :rtype: telium.TeliumResponse|None
        """

        answer = None  # Initializing null variable.

        # Set high timeout in order to wait for device to answer us.
        self._device.timeout = DELAI_REPONSE_TERMINAL_PAIEMENT

        # We wait for terminal to answer us.
        if self._wait_signal('ENQ'):

            self._send_signal('ACK')  # We're about to say that we're ready to accept data.

            if telium_ask.answer_flag == TERMINAL_ANSWER_SET_FULLSIZED:
                answer = self._read_answer(TERMINAL_ANSWER_COMPLETE_SIZE)
            elif telium_ask.answer_flag == TERMINAL_ANSWER_SET_SMALLSIZED:
                answer = self._read_answer(TERMINAL_ANSWER_LIMITED_SIZE)
            else:
                raise TerminalUnrecognizedConstantException(
                    "Cannot determine expected answer size because answer flag is unknown.")

            self._send_signal('ACK')  # Notify terminal that we've received it all.

            # The terminal should respond with EOT aka. End of Transmission.
            if not self._wait_signal('EOT'):
                raise TerminalUnexpectedAnswerException(
                    "Terminal should have ended the communication with 'EOT'. Something's obviously wrong.")
        else:  # If device has answered something different than ENQ like NAK for instance.
            self._send_signal('EOT')

        self._device.timeout = 1
        return answer
