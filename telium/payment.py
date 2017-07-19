import json
from functools import reduce
from operator import xor
from abc import ABCMeta, abstractmethod
import curses.ascii
from pycountry import currencies
from payment_card_identifier import CardIdentifier
from telium.constant import TERMINAL_PAYMENT_SUCCESS, TERMINAL_ANSWER_COMPLETE_SIZE, TERMINAL_ANSWER_LIMITED_SIZE, \
    TERMINAL_ASK_REQUIRED_SIZE, TERMINAL_DATA_ENCODING


class LrcChecksumException(Exception):
    pass


class SequenceDoesNotMatchLengthException(Exception):
    pass


class TeliumData(metaclass=ABCMeta):
    """
    Base class for Telium Manager packet struct.
    Shouldn't be used as is. Use TeliumAsk or TeliumResponse.
    """

    def __init__(self, pos_number, amount, payment_mode, currency_numeric, private):
        """
        :param str pos_number: Checkout ID, min 1, max 99.
        :param float amount: Payment amount, min 0.01, max 99999.99.
        :param str payment_mode: Type of payment support, please refers to provided constants.
        :param str currency_numeric: Type of currency ISO format, please use specific setter.
        :param str private:
        """
        self._pos_number = pos_number
        self._payment_mode = payment_mode
        self._currency_numeric = currency_numeric
        self._amount = amount
        self._private = private

    @property
    def pos_number(self):
        """
        Indicate your checkout id
        :return: Checkout id
        :rtype: str
        """
        return self._pos_number.zfill(2)

    @property
    def payment_mode(self):
        """
        Set default payment mode, DEBIT, CREDIT, REFUND or AUTO.
        :return: Payment mode
        :rtype: str
        """
        return self._payment_mode

    @property
    def currency_numeric(self):
        return self._currency_numeric

    @currency_numeric.setter
    def currency_numeric(self, currency):
        self._currency_numeric = str(currencies.get(alpha_3=currency.upper()).numeric).zfill(3)

    @property
    def private(self):
        """
        Unique transaction id if supported by device.
        :return: Transaction UUID
        :rtype: str
        """
        return self._private

    @property
    def amount(self):
        """
        Payment amount
        :return: Amount
        :rtype: float
        """
        return self._amount

    @staticmethod
    def lrc(data):
        """
        Calc. LRC from data. Checksum
        :param bytes|str data: Data from which LRC checksum should be computed
        :return: 0x00 < Result < 0xFF
        :rtype: int
        """
        if isinstance(data, str):
            data = data.encode(TERMINAL_DATA_ENCODING)
        return reduce(xor, [c for c in data])

    @staticmethod
    def lrc_check(data):
        """
        Verify if a chunk of data from terminal has a valid LRC checksum.
        :param data: raw data from terminal
        :return: True if LRC was verified
        :rtype: bool
        """
        return TeliumData.lrc(data[1:-1]) == data[-1]

    @abstractmethod
    def encode(self):
        return NotImplemented

    @staticmethod
    @abstractmethod
    def decode(data):
        """
        Create TeliumData instance from raw bytes data
        :param bytes data: raw sequence from terminal
        :return: New exploitable instance from raw data
        """
        return NotImplemented

    @property
    def __dict__(self):
        return {
            '_pos_number': self.pos_number,
            '_payment_mode': self.payment_mode,
            '_currency_numeric': self.currency_numeric,
            '_amount': self.amount,
            '_private': self.private
        }

    @property
    def json(self):
        """
        Serialize instance to JSON string
        :return: JSON representation-like of instance
        :rtype: str
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class TeliumAsk(TeliumData):
    def __init__(self, pos_number, answer_flag, transaction_type, payment_mode, currency_numeric, delay, authorization,
                 amount):
        super(TeliumAsk, self).__init__(pos_number, amount, payment_mode, currency_numeric, ' ' * 10)
        self._answer_flag = answer_flag
        self._transaction_type = transaction_type
        self._payment_mode = payment_mode
        self._delay = delay
        self._authorization = authorization

    @property
    def answer_flag(self):
        """
        Whenever ask for extended data in answer.
        Should correspond to one of the provided constants.
        :return: '1' or '0'
        :rtype: str
        """
        return self._answer_flag

    @property
    def transaction_type(self):
        return self._transaction_type

    @property
    def delay(self):
        """
        Describe if answer should be immediate (without valid status) or after transaction.
        :return: 'A010' | 'A011'
        :rtype: str
        """
        return self._delay

    @property
    def authorization(self):
        """
        Describe if the terminal has to manually authorize payment.
        TERMINAL_FORCE_AUTHORIZATION_ENABLE: 'B011'
        TERMINAL_FORCE_AUTHORIZATION_DISABLE: 'B010'
        :return: 'B011' | 'B010'
        :rtype: str
        """
        return self._authorization

    def encode(self):
        """
        Transform current object so it could be transfered to device (Protocol E)
        :return: Str raw array with payment information
        :rtype: str
        """
        packet = (

            str(self.pos_number) +  # 2 octets  0:3

            ('%.0f' % (self.amount * 100)).zfill(8) +  # 8 octets  3:11

            self.answer_flag +  # 1 octet 11:12

            self.payment_mode +  # 1 octet 12:13

            self.transaction_type +  # 1 octet 13:14

            self.currency_numeric +  # 3 octet 14:17

            self.private +  # 10 octet 17:27

            self.delay +  # 4 octet 27:31

            self.authorization)  # 4 octet 31:35

        packet_len = len(packet)

        if packet_len != TERMINAL_ASK_REQUIRED_SIZE:
            raise SequenceDoesNotMatchLengthException('Cannot create ask payment sequence with len != {0} octets. '
                                                      'Currently have {1} octet(s).'.format
                                                      (TERMINAL_ASK_REQUIRED_SIZE, packet_len))

        packet += chr(curses.ascii.controlnames.index('ETX'))

        return chr(curses.ascii.controlnames.index('STX')) + packet + chr(TeliumData.lrc(packet))

    @staticmethod
    def decode(data):
        """
        Create TeliumAsk from raw str include ETX.....STX.LRC
        :param bytes data: Raw bytes sequence.
        :return: TeliumAsk
        :rtype: telium.TeliumAsk
        """
        if TeliumData.lrc_check(data) is False:
            raise LrcChecksumException('Cannot decode data with erroned LRC check.')

        raw_message = data[1:-2].decode(TERMINAL_DATA_ENCODING)

        data_len = len(raw_message)

        if data_len != TERMINAL_ASK_REQUIRED_SIZE:
            raise SequenceDoesNotMatchLengthException('Cannot decode ask payment sequence with len != {0} octets. '
                                                      'Currently have {1} octet(s).'.format(
                                                          TERMINAL_ASK_REQUIRED_SIZE, data_len))

        return TeliumAsk(
            raw_message[0:2],  # pos_number
            raw_message[10],  # answer_flag
            raw_message[12],  # transaction_type
            raw_message[11],  # payment_mode
            raw_message[13:16],  # currency_numeric
            raw_message[26:30],  # delay
            raw_message[30:34],  # authorization
            float(raw_message[2:8] + '.' + raw_message[8:10])  # amount
        )

    @property
    def __dict__(self):

        new_dict = super().__dict__

        new_dict.update({
            '_answer_flag': self.answer_flag,
            '_transaction_type': self.transaction_type,
            '_payment_mode': self.payment_mode,
            '_delay': self.delay,
            '_authorization': self.authorization
        })

        return new_dict


class TeliumResponse(TeliumData):
    def __init__(self, pos_number, transaction_result, amount, payment_mode, repport, currency_numeric, private):
        super(TeliumResponse, self).__init__(pos_number, amount, payment_mode, currency_numeric, private)
        self._transaction_result = transaction_result
        self._repport = repport if repport is not None else ''
        self._card_type = next((result for result in [CardIdentifier.from_numbers(self._repport[:10+i]) for i in range(13)] if result is not None), None)

    @property
    def transaction_result(self):
        """
        TERMINAL_PAYMENT_SUCCESS: 0
        TERMINAL_PAYMENT_REJECTED: 7
        TERMINAL_PAYMENT_TIMEOUT: 9
        :return: Result provided after transaction. Should'nt be different than 0, 7 or 9.
        :rtype: int
        """
        return self._transaction_result

    @property
    def repport(self):
        """
        Contain data like the card numbers for instance.
        Should be handled wisely.
        :return: RAW Repport
        :rtype: str
        """
        return self._repport if self._repport is not None else ''

    @property
    def has_succeeded(self):
        """
        Verify if payment has been succesfuly processed.
        :return: True if payment has been approved
        :rtype: bool
        """
        return self.transaction_result == TERMINAL_PAYMENT_SUCCESS

    @property
    def card_type(self):
        """
        Return if available payment card type
        :return: Card type if available
        :rtype: PaymentCard|None
        """
        return self._card_type

    @property
    def card_id(self):
        """
        Read card numbers if available.
        Return PaymentCard instance.
        :return: Card numbers
        :rtype: str
        """
        return self._card_type.numbers if self._card_type is not None else self._repport

    @property
    def transaction_id(self):
        """
        Return transaction id generated by device if available.
        This method is an alias of self.private
        :return: Transaction unique id.
        :rtype: str
        """
        return self.private

    def encode(self):
        """
        Test purpose only. No use in production env.
        :return: Str message to be sent to master
        :rtype: str
        """

        packet = (

            str(self.pos_number) +  # 2 octets

            str(self.transaction_result) +  # 1 octet

            ('%.0f' % (self.amount * 100)).zfill(8) +  # 8 octets

            str(self.payment_mode) +  # 1 octet

            str(self.repport) +  # 55 octets

            str(self.currency_numeric) +  # 3 octets

            str(self.private)  # 10 octets

        )

        packet_len = len(packet)

        if packet_len not in [TERMINAL_ANSWER_COMPLETE_SIZE - 3, TERMINAL_ANSWER_LIMITED_SIZE - 3]:
            raise SequenceDoesNotMatchLengthException(
                'Cannot create response payment sequence with len != {0} or {1} octet(s) '
                'Currently have {2} octet(s).'.format(TERMINAL_ANSWER_COMPLETE_SIZE - 3, TERMINAL_ANSWER_LIMITED_SIZE - 3, packet_len))

        packet += chr(curses.ascii.controlnames.index('ETX'))

        return chr(curses.ascii.controlnames.index('STX')) + packet + chr(TeliumData.lrc(packet))

    @staticmethod
    def decode(data):
        """
        Create TeliumResponse from raw bytes array
        :param bytes data: Raw bytes answer from terminal
        :return: New instance of TeliumResponse from raw bytes sequence.
        :rtype: telium.TeliumResponse
        """

        if TeliumData.lrc_check(data) is False:
            raise LrcChecksumException('Cannot decode data with erroned LRC check.')

        raw_message = data[1:-2].decode(TERMINAL_DATA_ENCODING)
        data_size = len(data)

        if data_size == TERMINAL_ANSWER_COMPLETE_SIZE:
            return TeliumResponse(
                raw_message[0:2],
                int(raw_message[2]),
                float(raw_message[3:9] + '.' + raw_message[9:11]),
                raw_message[11],
                raw_message[12:67],
                raw_message[67:70],
                raw_message[70:80]
            )
        elif data_size == TERMINAL_ANSWER_LIMITED_SIZE:
            return TeliumResponse(
                raw_message[0:2],
                int(raw_message[2]),
                float(raw_message[3:9] + '.' + raw_message[9:11]),
                raw_message[11],
                '',
                raw_message[12:15],
                raw_message[15:25]
            )
        raise SequenceDoesNotMatchLengthException('Cannot decode raw sequence with length = {0}, '
                                                  'should be {1} octet(s) or {2} octet(s) long.'
                                                  .format(data_size, TERMINAL_ANSWER_COMPLETE_SIZE,
                                                          TERMINAL_ANSWER_LIMITED_SIZE))

    @property
    def __dict__(self):

        new_dict = super().__dict__  # Copying parent __dict__

        new_dict.update({  # Merge the parent one with this new one
            'has_succeeded': self.has_succeeded,
            'transaction_id': self.transaction_id,
            '_transaction_result': self.transaction_result,
            '_repport': self.repport,
            '_card_type': {
                '_name': self.card_type.name,
                '_regex': self.card_type.regex.pattern,
                '_numbers': self.card_type.numbers,
                '_masked_numbers': self.card_type.masked_numbers()
            } if self.card_type is not None else None
        })

        return new_dict  # Return new dict
