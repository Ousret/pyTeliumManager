.. pyTeliumManager documentation master file, created by
   sphinx-quickstart on Fri Jun 16 04:30:35 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
 pyTeliumManager
===============

Overview
========

This module allow you to manipulate your Ingenico payment device such as IWL250, iCT250 for instance.

It is released under MIT license, see LICENSE for more
details. Be aware that no warranty of any kind is provided with this package.

Copyright (C) 2017 Ahmed TAHRI <ahmed(at)tahri.space>

Features
========

- Ask for payment in any currency.
- Verify transaction afterward.

Requirements
============

This package is meant to be cross-plateform. Unix, Linux and NT systems are supported.

Libs
----

- Python >= 3.0 is recommanded, hasn't been tested on 2.7 yet.
- pySerial >= 3.3
- pyCountry >= 17.0

Device
------

In order to accept communication of any kind, your device must be configured to.

1. Press "F" button.
2. Press 0 - Telium Manager
3. Press 5 - Init.
4. Press 1 - Settings
5. Select  - Cashdraw/Checkout connect.
6. Select "Enable"
7. Then select your prefered interface (USB, COM1, COM2)

Afterward, you should reboot your device.

Installation
============

This installs a package that can be used from Python (``import telium``).

To install for all users on the system, administrator rights (root)
may be required.

From PyPI
---------
pyTeliumManager can be installed from PyPI::

    pip install pyTeliumManager

From git via dev-master
-----------------------
You can use dev-master branch from remote git to install it::

    git clone https://github.com/Ousret/pyTeliumManager.git
    cd pyTeliumManager/
    python setup.py install


Classes
=======

Transaction details
-------------------

.. class:: TeliumAsk

    .. method:: __init__(pos_number, answer_flag, transaction_type, payment_mode, currency_numeric, delay, authorization, amount)

        :param str pos_number:
            Checkout unique identifier from '01' to '99'.
        :param str answer_flag:
            Answer repport size. use :const:`TERMINAL_ANSWER_SET_FULLSIZED` for complete details or :const:`TERMINAL_ANSWER_SET_SMALLSIZED`
            for limited answer repport. Limited answer size won't show payment source id like credit card numbers.
        :param str transaction_type:
            If transaction is about CREDIT, DEBIT, etc.. .
            Use at least one of listed possible values:
            :const:`TERMINAL_MODE_PAYMENT_DEBIT`,
            :const:`TERMINAL_MODE_PAYMENT_CREDIT`,
            :const:`TERMINAL_MODE_PAYMENT_REFUND`,
            :const:`TERMINAL_MODE_PAYMENT_AUTO`.
        :param str payment_mode:
            Type of payment support.
            Use at least one of listed possible values:
            :const:`TERMINAL_TYPE_PAYMENT_CARD`,
            :const:`TERMINAL_TYPE_PAYMENT_CHECK`,
            :const:`TERMINAL_TYPE_PAYMENT_AMEX`,
            :const:`TERMINAL_TYPE_PAYMENT_CETELEM`,
            :const:`TERMINAL_TYPE_PAYMENT_COFINOGA`,
            :const:`TERMINAL_TYPE_PAYMENT_DINERS`,
            :const:`TERMINAL_TYPE_PAYMENT_FRANFINANCE`,
            :const:`TERMINAL_TYPE_PAYMENT_JCB`,
            :const:`TERMINAL_TYPE_PAYMENT_ACCORD_FINANCE`,
            :const:`TERMINAL_TYPE_PAYMENT_MONEO`,
            :const:`TERMINAL_TYPE_PAYMENT_CUP`,
            :const:`TERMINAL_TYPE_PAYMENT_FINTRAX_EMV`,
            :const:`TERMINAL_TYPE_PAYMENT_OTHER`.
        :param str currency_numeric:
            Currency ISO format.
            Two ISO currency are available as constant.
            :const:`TERMINAL_NUMERIC_CURRENCY_EUR`: EUR - € - ISO;978.
            :const:`TERMINAL_NUMERIC_CURRENCY_USD`: USD - $ - ISO;840.
        :param str delay:
            Describe if answer should be immediate (without valid status) or after transaction.
            Use at least one of listed possible values:
            :const:`TERMINAL_REQUEST_ANSWER_WAIT_FOR_TRANSACTION`,
            :const:`TERMINAL_REQUEST_ANSWER_INSTANT`.
        :param str authorization:
            Describe if the terminal has to manually authorize payment.

            Use at least one of listed possible values:
            :const:`TERMINAL_FORCE_AUTHORIZATION_ENABLE`,
            :const:`TERMINAL_FORCE_AUTHORIZATION_DISABLE`.
        :param float amount:
            Payment amount, min 0.01, max 99999.99.

        This object is meant to be translated into a bytes sequence and transfered to your terminal.

    .. method:: encode()

        :return: Raw string array with payment information
        :rtype: str
        :exception SequenceDoesNotMatchLengthException:
            Will be raised if the string sequence doesn't match required length. This mean you should check your instance params.

        Translate object into a string sequence ready to be sent to device.

    .. staticmethod:: decode(data)

        :param bytes data: Raw bytes sequence to be converted into TeliumAsk instance.
        :return: Create a new TeliumAsk.
        :rtype: TeliumAsk
        :exception LrcChecksumException:
            Will be raised if LRC checksum doesn't match.
        :exception SequenceDoesNotMatchLengthException:
            Will be raised if the string sequence doesn't match required length.

        Create a new instance of TeliumAsk from a bytes sequence previously generated with encode().
        This as no use in a production environnement.

Device management
-----------------

.. class:: Telium

    .. method:: __init__(path='/dev/ttyACM0', baudrate=9600, timeout=1)

        :param path:
            Device path.

        :param int baudrate:
            Baud rate such as 9600 or 115200 etc.
            Constructor do recommand to set it as 9600.

        :param float timeout:
            Set a read timeout value.

        The port is immediately opened on object creation.

        *path* is the device path: depending on operating system. e.g.
        ``/dev/ttyACM0`` on GNU/Linux or ``COM3`` on Windows. Please be aware
        that you'll need proper driver on Windows in order to create an emulated serial device.

        Possible values for the parameter *timeout* which controls the behavior
        of the device instance:

        - ``timeout = None``:  wait forever / until requested number of bytes
          are received, not recommanded.
        - ``timeout = 0``:     non-blocking mode, return immediately in any case,
          returning zero or more, up to the requested number of bytes, use it only when your computer is really fast unless
          you doesn't care about reliability.
        - ``timeout = x``:     set timeout to ``x`` seconds (float allowed)
          returns immediately when the requested number of bytes are available,
          otherwise wait until the timeout expires and return all bytes that
          were received until then.

    .. staticmethod:: get()

        :return: Fresh new Telium instance or None
        :rtype: Telium|None

        Auto-create a new instance of Telium. The device path will be infered based on most commom location.
        This won't be reliable if you have more than one emulated serial device plugged-in. Won't work either on NT plateform.

    .. method:: ask(telium_ask)

        :param TeliumAsk telium_ask: Payment details
        :return: True if device has accepted it, False otherwise.
        :rtype: bool

        Initialize payment to terminal

    .. method:: verify(telium_ask)

        :param TeliumAsk telium_ask: Payment details previously used on ask()
        :return: Transaction results as TeliumResponse, None if nothing was catched from device.
        :rtype: TeliumResponse|None

        Wait for answer and convert it to TeliumResponse for you.

    .. method:: close()

        Close device if currently opened. Recommanded practice, don't let Python close it from garbage collector.

Example
=======

Most basic usage
----------------

Example of usage::

    # Open device
    my_device = Telium('/dev/ttyACM0')

    # Construct our payment infos
    my_payment = TeliumAsk(
        '1',  # Checkout ID 1
        TERMINAL_ANSWER_SET_FULLSIZED,  # Ask for fullsized repport
        TERMINAL_MODE_PAYMENT_DEBIT,  # Ask for debit
        TERMINAL_TYPE_PAYMENT_CARD,  # Using a card
        TERMINAL_NUMERIC_CURRENCY_EUR,  # Set currency to EUR
        TERMINAL_REQUEST_ANSWER_WAIT_FOR_TRANSACTION,  # Wait for transaction to end before getting final answer
        TERMINAL_FORCE_AUTHORIZATION_DISABLE,  # Let device choose if we should ask for authorization
        12.5  # Ask for 12.5 EUR
    )

    # Send payment infos to device
    my_device.ask(my_payment)

    # Wait for terminal to answer
    my_answer = my_device.verify(my_payment)

    if my_answer is not None:
        # Print answered data from terminal
        print(my_answer.__dict__)

.. toctree::
   :maxdepth: 2
   :caption: Contents:
