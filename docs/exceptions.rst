Exceptions
==========

.. exception:: SignalDoesNotExistException

    Trying to send a unknown signal to device.

.. exception:: DataFormatUnsupportedException

    Exception raised when trying to send something other than a string sequence to device.

.. exception:: TerminalInitializationFailedException

    Exception raised when your device doesn't respond with 'ACK' signal when receiving 'ENQ' signal.
    Could mean that the device is busy or not well configured.

.. exception:: TerminalUnrecognizedConstantException

    Exception raised when you've built a TeliumAsk instance without proposed constant from package.

.. exception:: LrcChecksumException

    Exception raised when your raw bytes sequence does not match computed LRC with actual one from the sequence.
    Could mean that your serial/usb conn isn't stable.

.. exception:: SequenceDoesNotMatchLengthException

    Exception raised when trying to translate object via encode() or decode() doesn't match required output length.
    Could mean that your device is currently unsupported.

.. exception:: IllegalAmountException

    Exception raised when asking for an amount is bellow TERMINAL_MINIMAL_AMOUNT_REQUESTABLE and higher than TERMINAL_MAXIMAL_AMOUNT_REQUESTABLE.