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
        TERMINAL_ANSWER_SET_FULLSIZED,  # Ask for fullsized report
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

Create TeliumAsk instance from static method
--------------------------------------------

Create instance::

    my_payment = TeliumAsk.new_payment(
        12.5,  # Amount you want
        payment_mode='debit',  # other mode: credit or refund.
        target_currency='EUR',
        wait_for_transaction_to_end=True,  # If you need valid transaction status
        collect_payment_source_info=True,  # If you need to identify payment source
        force_bank_verification=False   # Set it to True if you absolutly need more guarantee in this transaction. Could result in slower authorization from bank.
    )

Use Ingenico payment device thought not emulated serial link
------------------------------------------------------------

.. image:: https://pmcdn.priceminister.com/photo/ingenico-sagem-cable-liaison-1m-vers-pc-ou-caisse-rs232-femelle-et-rj11-1033614629_ML.jpg
   :height: 200px
   :width: 300px
   :scale: 50 %
   :alt: Ingenico RS 232 Cable
   :align: left

Init::

    # It's as easy as this
    my_device = TeliumNativeSerial('/dev/ttyS4')
