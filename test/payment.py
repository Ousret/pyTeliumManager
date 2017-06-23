from unittest import TestCase, main
from telium import *

class TestTPE(TestCase):

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

        my_payment_proto_e = my_payment.toProtoE()

        self.assertEqual(len(my_payment_proto_e), 37, 'TeliumAsk encoded ProtoE should be 37 octets long.')
        self.assertEqual(len(my_payment_proto_e[1:-2]), 34, 'TeliumAsk encoded ProtoE should be 34 octets long without STX..LRC..ETX')

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

        my_payment_proto_e = my_payment.toProtoE()[1:-2]

        my_payment_restored = TeliumAsk.decode(my_payment_proto_e)

        self.assertEqual(my_payment_restored.pos_number, my_payment.pos_number, 'pos_number is not equal from original to decoded')
        self.assertEqual(my_payment_restored.private, my_payment.private, 'private is not equal from original to decoded')
        self.assertEqual(my_payment_restored.answer_flag, my_payment.answer_flag, 'answer_flag is not equal from original to decoded')
        self.assertEqual(my_payment_restored.payment_mode, my_payment.payment_mode, 'payment_mode is not equal from original to decoded')
        self.assertEqual(my_payment_restored.amount, my_payment.amount, 'amount is not equal from original to decoded')
        self.assertEqual(my_payment_restored.delay, my_payment.delay, 'delay is not equal from original to decoded')
        self.assertEqual(my_payment_restored.currency_numeric, my_payment.currency_numeric, 'currency_numeric is not equal from original to decoded')


if __name__ == '__main__':
    main()