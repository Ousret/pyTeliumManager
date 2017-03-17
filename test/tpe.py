import unittest
from telium.manager import Telium


class TestTPE(unittest.TestCase):
    def test_demande_paiement(self):
        my_telium_instance = Telium(1, True, False, '/dev/tty.usbmodem1411')
        self.assertEqual(my_telium_instance.demande_paiement('my-payment-uuid', 0.5), True)


if __name__ == '__main__':
    unittest.main()
