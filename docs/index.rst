.. pyTeliumManager documentation master file, created by
   sphinx-quickstart on Fri Jun 16 04:30:35 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========
 pyTeliumManager
==========

Overview
========

This module allow you to manipulate your Ingenico payment device such as IWL250, iCT250 for instance.

It is released under MIT license, see LICENSE_ for more
details. Be aware that no warranty of any kind is provided with this package.

Copyright (C) 2017 Ahmed TAHRI <ahmed(at)tahri.space>

Features
========

- Ask for payment in any currency.
- Verify transaction afterward.

Requirements
============
- Python >= 3.0 is recommanded, hasn't been tested on 2.7
- pySerial
- pyCountry >= 17.0
- Any operating system that can execute Python. That said, I've tested it on Unix, Linux and NT.


Device
===========

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


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
