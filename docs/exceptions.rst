Exceptions
==========

.. exception:: SignalDoesNotExistException

    Trying to send a unknown signal to device.

.. exception:: DataFormatUnsupportedException

    Exception that is raised when trying to send something else than string sequence to device.

.. exception:: TerminalInitializationFailedException

    Exception that is raised when your device doesn't respond with 'ACK' signal when receiving 'ENQ' signal.
    Could mean that the device is busy or not well configured.

.. exception:: TerminalUnrecognizedConstantException

    Exception that is raised when you've built a TeliumAsk instance without proposed constant from package.

.. exception:: LrcChecksumException

    Exception raised when your raw bytes sequence doesn't not match computed LRC with actual on from the sequence.
    Could mean that your serial/usb conn isn't stable.

.. exception:: SequenceDoesNotMatchLengthException

    Exception that is raised when trying to translate object via encode() or decode() doesn't match required output length.
    Could mean that your device is currently unsupported.
