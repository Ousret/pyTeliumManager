## **pyTeliumManager**
![Travis-CI](https://travis-ci.org/Ousret/pyTeliumManager.svg?branch=master) [![codecov](https://codecov.io/gh/Ousret/pyTeliumManager/branch/master/graph/badge.svg)](https://codecov.io/gh/Ousret/pyTeliumManager) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/ff5c954c3c2348ce8f3a1b7bd76e964c)](https://www.codacy.com/app/Ousret/pyTeliumManager?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Ousret/pyTeliumManager&amp;utm_campaign=Badge_Grade)

![iCT220-Terminal](http://www.tpe.fr/contents/media/ict220%201%20ls%20%2B%20ipp220.jpg)

_Python library to manipulate Ingenico mobile payment device equipped with Telium Manager. RS232/USB._
_Please note that every payment device with Telium Manager should, in theory, work with this._

##### PyPi

```sh
pip install pyTeliumManager --upgrade
```

##### How to start using pyTeliumManager

```python
# Import telium package
from telium import *

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
try:
    if not my_device.ask(my_payment):
        print('Unable to init payment on device.')
        exit(1)
except TerminalInitializationFailedException as e:
    print(format(e))
    exit(2)

# Wait for terminal to answer
my_answer = my_device.verify(my_payment)

if my_answer is not None:
    # Print answered data from terminal
    print(my_answer.__dict__)
    
    # > {
    # '_pos_number': '01', 
    # '_payment_mode': '1', 
    # '_currency_numeric': '978', 
    # '_amount': 12.5, 
    # '_private': '0000000000', 
    # 'has_succeeded': True, 
    # 'transaction_id': '0000000000', 
    # '_transaction_result': 0, 
    # '_repport': '4711690463168807000000000000000000000000000000000000000', 
    # '_card_type': 
    #  {
    #      '_name': 'VISA', 
    #      '_regex': '^4[0-9]{12}(?:[0-9]{3})?$', 
    #      '_numbers': '4711690463168807', 
    #      '_masked_numbers': 'XXXXXXXXXXXX8807'
    #  }
    # }

if my_answer.has_succeeded:
    print("Your payment has been processed using a {0} card. Id: {1}".format(my_answer.card_type.name, my_answer.card_type.numbers))
else:
    print("Your payment was rejected. Try again if you wish to.")
```

##### **How to enable computer liaison with Ingenico device**

1. Press "F" button
2. Press 0 - Telium Manager
3. Press 5 - Init
4. Press 1 - Param
5. Select  - Checkout
6. Select "Enable"
7. Choose your prefered interface (USB, COM1, COM2)

**Tested devices:**

- Ingenico iWL250
- Ingenico iCT220
- Ingenico iCT250

Should work with all i**2XX device equipped with Telium Manager app.
Feel free to repport issue if your device isn't compatible with this package.

**Won't work**

- All direct PinPad liaison, also known as iPP3XX. (WiP see issue #2)

#### Q-A

> Will this package cause loss of money in any way ?
- You shouldn't worry about that, I've deployed it for a different store in 2015. No loss has been reported yet.
- If you hesitate on how to use this package, feel free to ask me before using it.

> My device isn't working with this package.
- Make sure you've followed **How to enable computer liaison with Ingenico device** steps above beforehand.
- If you're on Windows, make sure you've installed the correct driver.
- Try every COM port, one by one.
- On Linux it should be located at */dev/ttyACM0*, if not run ```ls -l /dev/tty* | grep ACM``` to locate it.

#### Contributions

Feel free to propose pull requests. This project may be improved in many ways.
