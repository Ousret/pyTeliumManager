import unittest
from telium import *


class TestTPE(unittest.TestCase):
    def test_demande_paiement(self):
        my_telium_instance = Telium('/dev/ttyACM0')

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
        my_telium_instance.ask(my_payment)

        # Wait for terminal to answer
        my_answer = my_telium_instance.verify(my_payment)

        self.assertNotEqual(my_answer, None)


if __name__ == '__main__':
    unittest.main()
