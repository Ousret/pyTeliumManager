<h1 align="center">Welcome to Ingenico for Human 👋 <a href="https://twitter.com/intent/tweet?text=The%20Real%20First%20Universal%20Charset%20%26%20Language%20Detector&url=https://www.github.com/Ousret/pyTeliumManager&hashtags=python,ingenico,credit,cards,debit,developers"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"/></a></h1>

<p align="center">
  <sup>One of the few library that help you use this kind of hardware</sup><br>
  <a href="https://travis-ci.org/Ousret/pyTeliumManager">
    <img src="https://travis-ci.org/Ousret/pyTeliumManager.svg?branch=master"/>
  </a>
  <img src="https://img.shields.io/pypi/pyversions/pyTeliumManager.svg?orange=blue" />
  <a href="https://pepy.tech/project/pyTeliumManager/">
    <img alt="Download Count /Month" src="https://pepy.tech/badge/pyTeliumManager/month"/>
  </a>
  <a href="https://github.com/ousret/pyTeliumManager/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-purple.svg" target="_blank" />
  </a>
  <a href="https://app.codacy.com/project/Ousret/pyTeliumManager/dashboard">
    <img alt="Code Quality Badge" src="https://api.codacy.com/project/badge/Grade/ff5c954c3c2348ce8f3a1b7bd76e964c"/>
  </a>
  <a href="https://codecov.io/gh/Ousret/pyTeliumManager">
      <img src="https://codecov.io/gh/Ousret/pyTeliumManager/branch/master/graph/badge.svg" />
  </a>
  <a href='https://pyteliummanager.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/pyteliummanager/badge/?version=latest' alt='Documentation Status' />
  </a>
  <img alt="Download Count Total" src="https://pepy.tech/badge/pyTeliumManager" />
  <br>
  <img src="http://www.tpe.fr/contents/media/ict220%201%20ls%20%2B%20ipp220.jpg" width=200/>
</p>

> Python library to manipulate Ingenico mobile payment device equipped with Telium Manager. RS232/USB.
> Please note that every payment device with Telium Manager should, in theory, work with this.

##### PyPi

*Python 2.7 support has been added to master branch since v2.3.0*

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
my_payment = TeliumAsk.new_payment(
    12.5, 
    payment_mode='debit',  # other mode: credit or refund.
    target_currency='EUR',
    wait_for_transaction_to_end=True,  # If you need valid transaction status
    collect_payment_source_info=True,  # If you need to identify payment source
    force_bank_verification=False
)

# Send payment infos to device
try:
    if not my_device.ask(my_payment):
        print('Your device just refused your transaction. Try again.')
        exit(1)
except TerminalInitializationFailedException as e:
    print(format(e))
    exit(2)

# Wait for terminal to answer
my_answer = my_device.verify(my_payment)

if my_answer is not None:
    # Convert answered data to dict.
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
7. Choose your preferred interface (USB, COM1, COM2)

**Tested devices:**

- Ingenico iWL250
- Ingenico iCT220
- Ingenico iCT250

Should work with all i**2XX device equipped with Telium Manager app.
Feel free to repport issue if your device isn't compatible with this package.

**Won't work**

- All direct PinPad liaison, also known as iPP3XX. (see issue #2)

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
