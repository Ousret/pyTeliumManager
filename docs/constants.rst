Constants
=========

*Answer flag*

Fullsized report contains payment unique identifier like credit-card numbers, smallsized does not.

.. data:: TERMINAL_ANSWER_SET_FULLSIZED
.. data:: TERMINAL_ANSWER_SET_SMALLSIZED

*Transaction type*

.. data:: TERMINAL_MODE_PAYMENT_DEBIT
.. data:: TERMINAL_MODE_PAYMENT_CREDIT
.. data:: TERMINAL_MODE_PAYMENT_REFUND
.. data:: TERMINAL_MODE_PAYMENT_AUTO

*Payment mode*

.. data:: TERMINAL_TYPE_PAYMENT_CARD
.. data:: TERMINAL_TYPE_PAYMENT_CHECK
.. data:: TERMINAL_TYPE_PAYMENT_AMEX
.. data:: TERMINAL_TYPE_PAYMENT_CETELEM
.. data:: TERMINAL_TYPE_PAYMENT_COFINOGA
.. data:: TERMINAL_TYPE_PAYMENT_DINERS
.. data:: TERMINAL_TYPE_PAYMENT_FRANFINANCE
.. data:: TERMINAL_TYPE_PAYMENT_JCB
.. data:: TERMINAL_TYPE_PAYMENT_ACCORD_FINANCE
.. data:: TERMINAL_TYPE_PAYMENT_MONEO
.. data:: TERMINAL_TYPE_PAYMENT_CUP
.. data:: TERMINAL_TYPE_PAYMENT_FINTRAX_EMV
.. data:: TERMINAL_TYPE_PAYMENT_OTHER

*Delay*

Instant answer won't contain a valid transaction status.

.. data:: TERMINAL_REQUEST_ANSWER_WAIT_FOR_TRANSACTION
.. data:: TERMINAL_REQUEST_ANSWER_INSTANT

*Authorization*

Forced authorization control isn't recommended because it could be significantly slower.
You might have some ext. fees when using GPRS based payment device.

.. data:: TERMINAL_FORCE_AUTHORIZATION_ENABLE
.. data:: TERMINAL_FORCE_AUTHORIZATION_DISABLE
