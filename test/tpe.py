from unittest import TestCase, main
from telium import *
from test.fake_device import FakeTeliumDevice


class TestTPE(TestCase):

    def setUp(self):
        self._fake_device = FakeTeliumDevice()

    def test_demande_paiement(self):

        my_telium_instance = Telium(self._fake_device.s_name)

        # Construct our payment infos
        my_payment = TeliumAsk(
            '1',  # Checkout ID 1
            TERMINAL_ANSWER_SET_FULLSIZED,  # Ask for fullsized repport
            TERMINAL_MODE_PAYMENT_DEBIT,  # Ask for debit
            TERMINAL_TYPE_PAYMENT_CARD,  # Using a card
            TERMINAL_NUMERIC_CURRENCY_EUR,  # Set currency to EUR
            TERMINAL_REQUEST_ANSWER_WAIT_FOR_TRANSACTION,  # Do not wait for transaction end for terminal answer
            TERMINAL_FORCE_AUTHORIZATION_DISABLE,  # Let device choose if we should ask for authorization
            12.5  # Ask for 12.5 EUR
        )

        # Send payment infos to device
        self.assertTrue(my_telium_instance.ask(my_payment))

        my_answer = my_telium_instance.verify(my_payment)

        self.assertEqual(my_answer.transaction_result, 0)
        self.assertEqual(my_answer.currency_numeric, TERMINAL_NUMERIC_CURRENCY_EUR)
        self.assertEqual(my_answer.private, '0' * 10)


if __name__ == '__main__':
    main()
