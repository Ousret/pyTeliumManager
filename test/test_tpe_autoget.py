from unittest import TestCase, main
from telium import *
from os.path import exists


class TestTPEAutoGet(TestCase):

    def test_auto_get(self):

        for path in TERMINAL_PROBABLES_PATH:
            if exists(path):
                # Should not render None
                my_telium_instance = Telium.get()
                self.assertIsNotNone(my_telium_instance)
                my_telium_instance.close()
                return

        self.assertIsNone(Telium.get())


if __name__ == '__main__':
    main()