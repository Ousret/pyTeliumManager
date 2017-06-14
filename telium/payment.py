import json
from functools import reduce
from operator import xor
import curses.ascii
from pycountry import currencies


class TeliumData:

    def __init__(self, pos_number, amount, payment_mode, currency_numeric, private):
        self._pos_number = pos_number
        self._payment_mode = payment_mode
        self._currency_numeric = currency_numeric
        self._amount = amount
        self._private = private

    @property
    def pos_number(self):
        return self._pos_number

    @property
    def payment_mode(self):
        return self._payment_mode

    @property
    def currency_numeric(self):
        return self._currency_numeric

    @currency_numeric.setter
    def currency_numeric(self, currency):
        self._currency_numeric = str(currencies.get(alpha_3=currency.upper()).numeric).zfill(3)

    @property
    def private(self):
        return self._private

    @property
    def amount(self):
        return self._amount

    @staticmethod
    def lrc(data):
        if isinstance(data, str):
            data = data.encode('ascii')
        return reduce(xor, [c for c in data])

    def toProtoE(self):
        return bytes()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class TeliumAsk(TeliumData):

    def __init__(self, pos_number, answer_flag, transaction_type, payment_mode, currency_numeric, delay, authorization, amount):
        super(TeliumAsk, self).__init__(pos_number, amount, payment_mode, currency_numeric, ' ' * 10)
        self._answer_flag = answer_flag
        self._transaction_type = transaction_type
        self._payment_mode = payment_mode
        self._delay = delay
        self._authorization = authorization

    @property
    def answer_flag(self):
        return self._answer_flag

    @property
    def transaction_type(self):
        return self._transaction_type

    @property
    def delay(self):
        return self._delay

    @property
    def authorization(self):
        return self._authorization

    def toProtoE(self):
        """
        Transform current object so it could be transfered to device (Protocol E)
        :return: Bytes array with payment information
        :rtype: bytes
        """
        packet = (

            str(self.pos_number).zfill(2) +

            ('%.0f' % (self.amount * 100)).zfill(8) +

            self.answer_flag +

            self.payment_mode +

            self.transaction_type +

            self.currency_numeric +

            self.private +

            self.delay +

            self.authorization)

        if len(packet) != 34:
            raise Exception('Le paquet cible ne respecte pas la taille du protocol E Telium (!=34)')

        packet += chr(curses.ascii.controlnames.index('ETX'))

        return chr(curses.ascii.controlnames.index('STX')) + packet + chr(TeliumData.lrc(packet))


class TeliumResponse(TeliumData):

    def __init__(self, pos_number, transaction_result, amount, payment_mode, repport, currency_numeric, private):
        super(TeliumResponse, self).__init__(pos_number, amount, payment_mode, currency_numeric, private)
        self._transaction_result = transaction_result
        self._repport = repport

    @property
    def transaction_result(self):
        return self._transaction_result

    @property
    def repport(self):
        return self._repport

    @staticmethod
    def decode(data):
        """
        Create TeliumResponse from raw bytes array
        :param data: Raw bytes answer from terminal
        :return: TeliumResponse
        :rtype: telium.TeliumResponse
        """

        return TeliumResponse(
            str(data[0:2], 'ascii'),
            int(chr(data[2])),
            str(data[3:11], 'ascii'),
            chr(data[11]),
            str(data[12:67], 'ascii'),
            str(data[68:71], 'ascii'),
            str(data[72:82], 'ascii')
        )
