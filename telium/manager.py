from glob import glob

import six
from telium.hexdump import hexdump
from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, PARITY_EVEN, SEVENBITS

from telium.constant import *
from telium.payment import TeliumResponse


class SignalDoesNotExistException(KeyError):
    pass


class DataFormatUnsupportedException(TypeError):
    pass


class TerminalSerialLinkClosedException(IOError):
    pass


class TerminalInitializationFailedException(IOError):
    pass


class TerminalUnrecognizedConstantException(Exception):
    pass


class TerminalUnexpectedAnswerException(IOError):
    pass


class Telium:
    def __init__(self,
                 path='/dev/ttyACM0',
                 baudrate=9600,
                 bytesize=EIGHTBITS,
                 parity=PARITY_NONE,
                 stopbits=STOPBITS_ONE,
                 timeout=1,
                 open_on_create=True,
                 debugging=False):
        """
        Create Telium device instance
        :param str path: str Path to serial emulated device
        :param int baudrate: Set baud rate
        :param int timeout: Maximum delai before hanging out.
        :param bool open_on_create: Define if device has to be opened on instance creation
        :param bool debugging: Enable print device <-> host com trace. (stdout)
        """
        self._path = path
        self._baud = baudrate
        self._debugging = debugging
        self._device_timeout = timeout
        self._device = None

        self._device = Serial(
            self._path if open_on_create else None,
            baudrate=self._baud,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout
        )

        if not open_on_create:
            self._device.setPort(self._path)

    @staticmethod
    def get(baudrate=9600, timeout=1, open_on_create=True, debugging=False):
        """
        Auto-create a new instance of Telium. The device path will be infered based on most commom location.
        This won't be reliable if you have more than one emulated serial device plugged-in.
        Won't work either on NT plateform.
        :param int baudrate: Baudrate.
        :param int timeout: Timeout for byte signal waiting.
        :param bool open_on_create: If device should be opened on instance creation.
        :param bool debugging: Set it to True if you want to trace comm. between device and host. (stdout)
        :return: Fresh new Telium instance or None
        :rtype: telium.Telium
        """
        for path in TERMINAL_PROBABLES_PATH:
            probables = glob('%s*' % ''.join(filter(lambda c: not c.isdigit(), path)))
            if len(probables) == 1:
                return Telium(probables[0], baudrate, timeout, open_on_create, debugging)
        return None

    def __del__(self):
        if self._device.is_open:
            self._device.close()

    @property
    def debugging(self):
        return self._debugging

    @property
    def timeout(self):
        """
        Get current timeout value from pySerial device instance
        :return: Current timeout setting from device handled by pySerial
        :rtype: float
        """
        return self._device.timeout

    @timeout.setter
    def timeout(self, new_timeout):
        self._device_timeout = new_timeout
        self._device.timeout = self._device_timeout

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
        if signal not in CONTROL_NAMES:
            raise SignalDoesNotExistException("The ASCII '%s' code doesn't exist." % signal)
        if self._debugging:
            print('DEBUG :: try send_signal = ', signal)
        return self._send(chr(CONTROL_NAMES.index(signal))) == 1

    def _wait_signal(self, signal):
        """
        Read one byte from serial device and compare to expected.
        :param signal: str
        :return: True if received signal match
        :rtype: bool
        """
        one_byte_read = self._device.read(1)
        expected_char = CONTROL_NAMES.index(signal)

        if self._debugging and len(one_byte_read) == 1:
            print('DEBUG :: wait_signal_received = ', CONTROL_NAMES[one_byte_read[0] if six.PY3 else ord(one_byte_read[0])])

        return one_byte_read == (expected_char.to_bytes(1, byteorder='big') if six.PY3 else chr(expected_char))

    def _send(self, data):
        """
        Send data to terminal
        :param str data: string representation to convert and send
        :return: Lenght of data actually sent
        :rtype: int
        """
        if not isinstance(data, str):
            raise DataFormatUnsupportedException("Type {0} cannont be send to device. "
                                                 "Please use string when calling _send method.".format(str(type(data))))
        return self._device.write(data.encode(TERMINAL_DATA_ENCODING))

    def _read_answer(self, expected_size=TERMINAL_ANSWER_COMPLETE_SIZE):
        """
        Download raw answer and convert it to TeliumResponse
        :return: TeliumResponse
        :raise: TerminalUnexpectedAnswerException If data cannot be converted into telium.TeliumResponse
        :rtype: telium.TeliumResponse
        """
        raw_data = self._device.read(size=expected_size)
        data_len = len(raw_data)

        if self._debugging:
            print('<---------------------------- Chunk from Terminal :: {0} byte(s).'.format(data_len))
            hexdump(raw_data)
            print('----------------------------> End of Chunk from Terminal')

        if data_len != expected_size:
            raise TerminalUnexpectedAnswerException('Raw read expect size = {0} '
                                                    'but actual size = {1}.'.format(expected_size, data_len))

        if raw_data[0] != (CONTROL_NAMES.index('STX') if six.PY3 else chr(CONTROL_NAMES.index('STX'))):
            raise TerminalUnexpectedAnswerException(
                'The first byte of the answer from terminal should be STX.. Have %02x and except %02x (STX)' % (
                    raw_data[0], CONTROL_NAMES.index('STX')))
        if raw_data[-2] != (CONTROL_NAMES.index('ETX') if six.PY3 else chr(CONTROL_NAMES.index('ETX'))):
            raise TerminalUnexpectedAnswerException(
                'The byte before final of the answer from terminal should be ETX')

        return TeliumResponse.decode(raw_data)

    def ask(self, telium_ask, raspberry_pi=False):
        """
        Initialize payment to terminal
        :param telium.TeliumAsk telium_ask: Payment info
        :param bool raspberry_pi: Set it to True if you'r running Raspberry PI
        :return: True if device has accepted to begin a new transaction.
        :rtype: bool
        """

        if not self.is_open:
            raise TerminalSerialLinkClosedException("Your device isn\'t opened yet.")

        if raspberry_pi:
            self._device.timeout = 0.3
            self._device.read(size=1)
            self._device.timeout = self._device_timeout

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
            return False

        # End this communication
        self._send_signal('EOT')

        return True

    def verify(self, telium_ask, waiting_timeout=DELAY_TERMINAL_ANSWER_TRANSACTION, raspberry_pi=False):
        """
        Wait for answer and convert it for you.
        :param telium.TeliumAsk telium_ask: Payment info
        :param float waiting_timeout: Custom waiting delay in seconds before giving up on waiting ENQ signal.
        :param bool raspberry_pi: Set it to True if you'r running Raspberry PI
        :return: TeliumResponse, None or Exception
        :rtype: telium.TeliumResponse|None
        """

        if not self.is_open:
            raise TerminalSerialLinkClosedException("Your device isn\'t opened yet.")

        answer = None  # Initializing null variable.

        # Set high timeout in order to wait for device to answer us.
        self._device.timeout = waiting_timeout

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
            if not self._wait_signal('EOT') and not raspberry_pi:
                raise TerminalUnexpectedAnswerException(
                    "Terminal should have ended the communication with 'EOT'. Something's obviously wrong.")

        # Restore device's timeout
        self._device.timeout = self._device_timeout

        return answer


class TeliumNativeSerial(Telium):

    def __init__(self,
                 path,
                 baudrate=9600,
                 timeout=1,
                 open_on_create=True,
                 debugging=False):
        super(TeliumNativeSerial, self).__init__(
            path,
            baudrate=baudrate,
            bytesize=SEVENBITS,
            parity=PARITY_EVEN,
            stopbits=STOPBITS_ONE,
            timeout=timeout,
            open_on_create=open_on_create,
            debugging=debugging)
