from unittest import TestCase, main
from telium import *


class TestTPE(TestCase):

    def test_telium_ask_size_not_match(self):

        my_payment = TeliumAsk(
            '1',
            TERMINAL_ANSWER_SET_FULLSIZED,
            TERMINAL_MODE_PAYMENT_DEBIT,
            TERMINAL_TYPE_PAYMENT_CARD,
            TERMINAL_NUMERIC_CURRENCY_USD,
            'NOT USING SPECIFIED CONSTANT',
            TERMINAL_FORCE_AUTHORIZATION_DISABLE,
            666.66
        )

        with self.assertRaises(SequenceDoesNotMatchLengthException):
            my_payment.encode()

        my_answer = TeliumResponse(
            '1',
            TERMINAL_PAYMENT_SUCCESS,
            10.91,
            'NOT USING SPECIFIED CONSTANT',
            None,
            TERMINAL_NUMERIC_CURRENCY_USD,
            10 * '0'
        )

        with self.assertRaises(SequenceDoesNotMatchLengthException):
            my_answer.encode()

        raw_invalid_sequence = '0000000000'

        with self.assertRaises(SequenceDoesNotMatchLengthException):
            TeliumAsk.decode(bytes(raw_invalid_sequence + chr(TeliumAsk.lrc(raw_invalid_sequence[1:])), TERMINAL_DATA_ENCODING))

        with self.assertRaises(SequenceDoesNotMatchLengthException):
            TeliumResponse.decode(bytes(raw_invalid_sequence + chr(TeliumAsk.lrc(raw_invalid_sequence[1:])), TERMINAL_DATA_ENCODING))

    def test_telium_ask_currencies_setter(self):

        my_payment = TeliumAsk(
            '1',
            TERMINAL_ANSWER_SET_FULLSIZED,
            TERMINAL_MODE_PAYMENT_DEBIT,
            TERMINAL_TYPE_PAYMENT_CARD,
            TERMINAL_NUMERIC_CURRENCY_USD,
            TERMINAL_REQUEST_ANSWER_WAIT_FOR_TRANSACTION,
            TERMINAL_FORCE_AUTHORIZATION_DISABLE,
            666.66
        )

        my_payment.currency_numeric = 'EUR'

        self.assertEqual(my_payment.currency_numeric, TERMINAL_NUMERIC_CURRENCY_EUR)

        with self.assertRaises(KeyError):
            my_payment.currency_numeric = 'USSSD'

        with self.assertRaises(KeyError):
            my_payment.currency_numeric = 'EURO'

    def test_telium_data_decode(self):

        with self.assertRaises(LrcChecksumException):
            TeliumResponse.decode(b'ShouldNotBeDecoded')
        with self.assertRaises(LrcChecksumException):
            TeliumAsk.decode(b'ShouldNotBeDecoded')

    def test_telium_ask_proto_e_len(self):

        my_payment = TeliumAsk(
            '1',
            TERMINAL_ANSWER_SET_FULLSIZED,
            TERMINAL_MODE_PAYMENT_DEBIT,
            TERMINAL_TYPE_PAYMENT_CARD,
            TERMINAL_NUMERIC_CURRENCY_EUR,
            TERMINAL_REQUEST_ANSWER_WAIT_FOR_TRANSACTION,
            TERMINAL_FORCE_AUTHORIZATION_DISABLE,
            55.1
        )

        my_payment_proto_e = my_payment.encode()

        self.assertEqual(len(my_payment_proto_e), 37, 'TeliumAsk encoded ProtoE should be 37 octets long.')
        self.assertEqual(len(my_payment_proto_e[1:-2]), 34, 'TeliumAsk encoded ProtoE should be 34 octets long without STX..LRC..ETX')

    def test_telium_response_proto_e_len(self):
        my_answer = TeliumResponse(
            '1',
            TERMINAL_PAYMENT_SUCCESS,
            12.5,
            TERMINAL_MODE_PAYMENT_DEBIT,
            '0' * 55,
            TERMINAL_NUMERIC_CURRENCY_EUR,
            '0' * 10
        )

        self.assertEqual(len(my_answer.payment_mode), 1)
        self.assertEqual(len(my_answer.pos_number), 2)
        self.assertEqual(len(my_answer.private), 10)
        self.assertEqual(len(my_answer.currency_numeric), 3)

    def test_telium_answer_proto_decode(self):

        my_answer = TeliumResponse(
            '1',
            TERMINAL_PAYMENT_SUCCESS,
            12.5,
            TERMINAL_MODE_PAYMENT_DEBIT,
            '0' * 55,
            TERMINAL_NUMERIC_CURRENCY_EUR,
            '0' * 10
        )

        print(my_answer.json)

        my_answer_proto_e = my_answer.encode()

        my_answer_restored = TeliumResponse.decode(bytes(my_answer_proto_e, 'ascii'))

        self.assertEqual(my_answer_restored.pos_number, my_answer.pos_number)
        self.assertEqual(my_answer_restored.transaction_result, my_answer.transaction_result)
        self.assertEqual(my_answer_restored.repport, my_answer.repport)
        self.assertEqual(my_answer_restored.currency_numeric, my_answer.currency_numeric)
        self.assertEqual(my_answer_restored.payment_mode, my_answer.payment_mode)
        self.assertEqual(my_answer_restored.amount, my_answer.amount)
        self.assertEqual(my_answer_restored.private, my_answer.private)
        self.assertEqual(my_answer.card_id, '0'*55)
        self.assertEqual(my_answer.has_succeeded, True)
        self.assertEqual(my_answer.transaction_id, '0'*10)

    def test_telium_ask_proto_decode(self):
        my_payment = TeliumAsk(
            '1',
            TERMINAL_ANSWER_SET_FULLSIZED,
            TERMINAL_MODE_PAYMENT_DEBIT,
            TERMINAL_TYPE_PAYMENT_CARD,
            TERMINAL_NUMERIC_CURRENCY_EUR,
            TERMINAL_REQUEST_ANSWER_WAIT_FOR_TRANSACTION,
            TERMINAL_FORCE_AUTHORIZATION_DISABLE,
            55.1
        )

        my_payment_proto_e = my_payment.encode()

        my_payment_restored = TeliumAsk.decode(bytes(my_payment_proto_e, 'ascii'))

        self.assertEqual(my_payment_restored.pos_number, my_payment.pos_number, 'pos_number is not equal from original to decoded')
        self.assertEqual(my_payment_restored.private, my_payment.private, 'private is not equal from original to decoded')
        self.assertEqual(my_payment_restored.answer_flag, my_payment.answer_flag, 'answer_flag is not equal from original to decoded')
        self.assertEqual(my_payment_restored.payment_mode, my_payment.payment_mode, 'payment_mode is not equal from original to decoded')
        self.assertEqual(my_payment_restored.amount, my_payment.amount, 'amount is not equal from original to decoded')
        self.assertEqual(my_payment_restored.delay, my_payment.delay, 'delay is not equal from original to decoded')
        self.assertEqual(my_payment_restored.currency_numeric, my_payment.currency_numeric, 'currency_numeric is not equal from original to decoded')


if __name__ == '__main__':
    main()