from unittest import TestCase, main
from telium import *
from test.fake_device import FakeTeliumDevice


class TestTPE(TestCase):

    def setUp(self):
        self._fake_device = FakeTeliumDevice()

    def tearDown(self):
        self._fake_device.stop()

    def test_demande_paiement(self):

        my_telium_instance = Telium(self._fake_device.s_name)

        # Construct our payment infos
        my_payment = TeliumAsk(
            '1',  # Checkout ID 1
            TERMINAL_ANSWER_SET_FULLSIZED,  # Ask for fullsized repport
            TERMINAL_MODE_PAYMENT_DEBIT,  # Ask for debit
            TERMINAL_TYPE_PAYMENT_CARD,  # Using a card
            TERMINAL_NUMERIC_CURRENCY_EUR,  # Set currency to EUR
            TERMINAL_REQUEST_ANSWER_INSTANT,  # Do not wait for transaction end for terminal answer
            TERMINAL_FORCE_AUTHORIZATION_DISABLE,  # Let device choose if we should ask for authorization
            12.5  # Ask for 12.5 EUR
        )

        # Send payment infos to device
        self.assertTrue(my_telium_instance.ask(my_payment))


if __name__ == '__main__':
    main()
