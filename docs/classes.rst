Classes
=======

Transaction details
-------------------

.. class:: TeliumAsk

    .. method:: __init__(pos_number, answer_flag, transaction_type, payment_mode, currency_numeric, delay, authorization, amount)

        :param str pos_number:
            Checkout unique identifier from '01' to '99'.
        :param str answer_flag:
            Answer report size. use :const:`TERMINAL_ANSWER_SET_FULLSIZED` for complete details or :const:`TERMINAL_ANSWER_SET_SMALLSIZED`
            for limited answer report. Limited report does not show payment source id, e.g. credit card numbers.
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

        This object is meant to be translated into a bytes sequence and transferred to your terminal.

    .. method:: encode()

        :return: Raw string array with payment information
        :rtype: str
        :exception SequenceDoesNotMatchLengthException:
            Will be raised if the string sequence doesn't match required length. Check your instance params.

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
        This is no use in a production environment.

    .. staticmethod:: new_payment(amount, payment_mode='debit', target_currency='USD', checkout_unique_id='1', wait_for_transaction_to_end=True, collect_payment_source_info=True, force_bank_verification=False)

        :param float amount: Amount requested
        :param str payment_mode: Specify transaction type. (debit, credit or refund)
        :param str target_currency: Target currency, must be written in letters. (EUR, USD, etc..)
        :param str checkout_unique_id: Unique checkout identifer.
        :param bool wait_for_transaction_to_end: Set to True if you need valid transaction status otherwise, set it to False.
        :param bool collect_payment_source_info: If you want to retrieve specifics data about payment source identification.
        :param bool force_bank_verification: Set it to True if your business need to enforce payment verification.
        :return: Ready to use TeliumAsk instance
        :rtype: TeliumAsk

        Create new TeliumAsk in order to prepare payment.
        Most commonly used.

Transaction results
-------------------

.. class:: TeliumResponse

    .. method:: __init__(pos_number, transaction_result, amount, payment_mode, report, currency_numeric, private)

        :param str pos_number:
            Checkout unique identifier from '01' to '99'.
        :param int transaction_result:
            Transaction result.
        :param float amount:
            Payment authorized/acquired amount.
        :param str payment_mode:
            Type of payment support.
        :param str report:
            Contains payment source unique identifier like credit-card numbers when fullsized report is enabled.
        :param str currency_numeric:
            Currency ISO format.
        :param str private:
            If supported by your device, contains transaction unique identifier.

    .. attribute:: has_succeeded

        :getter: True if transaction has been authorized, False otherwise.
        :type: bool

    .. attribute:: report

        :getter: Contain data like the card numbers for instance. Should be handled wisely.
        :type: str

    .. attribute:: transaction_id

        :getter: If supported by your device, contains transaction unique identifier.
        :type: bool

    .. attribute:: card_id

        :getter: Read card numbers if available.
        :type: str|None

    .. attribute:: card_id_sha512

        :getter: Return payment source id hash repr (sha512)
        :type: str|None

    .. attribute:: card_type

        :getter: Return if available payment card type
        :type: payment_card_identifier.PaymentCard|None

Device management
-----------------

.. class:: Telium

    .. method:: __init__(path='/dev/ttyACM0', baudrate=9600, timeout=1, open_on_create=True, debugging=False)

        :param path:
            Device path.

        :param int baudrate:
            Baud rate such as 9600 or 115200 etc.
            Constructor do recommend to set it as 9600.

        :param float timeout:
            Set a read timeout value.

        :param bool open_on_create:
            Specify if device should be immedialty opened on instance creation.

        :param bool debugging:
            Set it to True if you want to diagnose your device. Will print to stdout bunch of useful data.

        The port is immediately opened on object creation if open_on_create toggle is True.

        *path* is the device path: depending on operating system. e.g.
        ``/dev/ttyACM0`` on GNU/Linux or ``COM3`` on Windows. Please be aware
        that a proper driver is needed on Windows in order to create an emulated serial device.

        Possible values for the parameter *timeout* which controls the behavior
        of the device instance:

        - ``timeout = None``:  wait forever / until requested number of bytes
          are received, not recommended.
        - ``timeout = 0``:     non-blocking mode, return immediately in any case,
          returning zero or more, up to the requested number of bytes, use it only when your computer is really fast unless
          you don't care about reliability.
        - ``timeout = x``:     set timeout to ``x`` seconds (float allowed)
          returns immediately when the requested number of bytes are available,
          otherwise wait until the timeout expires and return all bytes that
          were received until then.

    .. staticmethod:: get()

        :return: Fresh new Telium instance or None
        :rtype: Telium|None

        Auto-create a new instance of Telium. The device path will be inferred based on most common location.
        This won't be reliable if you have more than one emulated serial device plugged-in. Does not work on NT platform.

    .. method:: ask(telium_ask)

        :param TeliumAsk telium_ask: Payment details
        :return: True if device has accepted it, False otherwise.
        :rtype: bool

        Initialize payment to terminal

    .. method:: verify(telium_ask)

        :param TeliumAsk telium_ask: Payment details previously used on ask()
        :return: Transaction results as TeliumResponse, None if nothing was caught from device.
        :rtype: TeliumResponse|None

        Wait for answer and convert it to TeliumResponse.

    .. method:: close()

        :return: True if device was previously opened and now closed. False otherwise.
        :rtype: bool

        Close device if currently opened. Recommended practice, don't let Python close it from garbage collector.

    .. attribute:: timeout

        :getter: Current timeout set on read.
        :type: float


Native serial proxy class
-------------------------

*Use this class instead of Telium if you're using native serial conn, see examples.*

.. class:: TeliumNativeSerial