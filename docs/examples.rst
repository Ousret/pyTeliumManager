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

