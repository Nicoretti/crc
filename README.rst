Status
------

.. image:: https://travis-ci.org/Nicoretti/crc.svg?branch=master
    :target: https://travis-ci.org/Nicoretti/crc

.. image:: https://ci.appveyor.com/api/projects/status/1tkrwbp3tiv0ikib/branch/master?svg=true
    :target: https://ci.appveyor.com/project/Nicoretti/crc

.. image:: https://coveralls.io/repos/Nicoretti/crc/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/Nicoretti/crc?branch=master

.. image:: https://landscape.io/github/Nicoretti/crc/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Nicoretti/crc/master
    :alt: Code Health

.. image:: https://readthedocs.org/projects/py-crc/badge/?version=latest
    :target: http://py-crc.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://gemnasium.com/Nicoretti/crc.svg
    :target: https://gemnasium.com/Nicoretti/crc)
    :alt: Dependency Status


Overview
--------
The crc package provides provides support for the most common functionality to handle and calculate various kinds of crc checksums.
(e.g. Crc8, Crc16, Crc32)

Supported CRC Algorithms:

Requirements
------------
* Python 3.6 and newer

Installation
------------
TBD

Usage
------


Calculate and verify crc checksum using provided crc algorithm
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block::

    data = [0, 1, 2, 3, 4, 5 ]
    expected_checksum = 0xff
    crc_calculator = CrcCalculator(Crc8.CCITT)

    checksum = crc_calculator.calculate_checksum(data)

    assert checksum == expected_checksum
    assert crc_calculator.verfify_checksum(data, expected_checksum)


Calculate crc using the CrcRegister class
+++++++++++++++++++++++++++++++++++++++++

.. code-block::

    data = [0, 1, 2, 3, 4, 5 ]
    expected_checksum = 0xff
    crc_calculator = CrcCalculator(Crc8.CCITT)

Speed up calculation (TableBasedRegister)
+++++++++++++++++++++++++++++++++++++++++

.. code-block::

    data = [0, 1, 2, 3, 4, 5 ]
    expected_checksum = 0xff
    crc_calculator = CrcCalculator(Crc8.CCITT)


How to create a custom crc configuration
+++++++++++++++++++++++++++++++++++++++++

.. code-block::

    data = [0, 1, 2, 3, 4, 5 ]
    expected_checksum = 0xff
    crc_calculator = CrcCalculator(Crc8.CCITT)


Write your own CrcRegister based on CrcRegisterBase
+++++++++++++++++++++++++++++++++++++++++++++++++++

Based on CrcRegisterBase
------------------------

.. code-block::

    data = [0, 1, 2, 3, 4, 5 ]
    expected_checksum = 0xff
    crc_calculator = CrcCalculator(Crc8.CCITT)

Based on AbstractCrcRegister
----------------------------

.. code-block::

    data = [0, 1, 2, 3, 4, 5 ]
    expected_checksum = 0xff
    crc_calculator = CrcCalculator(Crc8.CCITT)


Command line tools
==================

cli extension point
+++++++++++++++++++
name:  crc.cli.command
description: TBD

crc
++++++++++++++++++++
A set of crc checksum related command line tools.

.. code-block::

    usage:
        crc [--version][--help] <command> [<args>...]

    options:

        -h, --help      prints this help dialoge
        --version       version

    commands:
        table       creates a crc lookup table.
        verfiy      verfies a already calcualted crc for the specified data.
        calcualte   calculates the crc checksum for the specified data.

table
-----
Command line tool to create crc lookup tables.

.. code-block::

    usage:
        crc table [options] <width> <polynom>

    arguments:
        <polynom>       hex value of the polynom used for calculating the crc table.

    options:
        -h, --help
        --version

verify
------
Not supported yet

calculate
---------
Not supported yet


Tips & Tricks
-------------
Info:
Main code -> crc.py works without any dependencies -> copy and paste into project
but gererally highly recommend -> install using pip -> tests etc


References & Resources
-----------------------
* `A Painless guide to crc error detection algorithms <http://www.zlib.net/crc_v3.txt>`_
* `Project on Github <https://github.com/Nicoretti/crc>`_
* `Online Crc calculator <>`_

http://reveng.sourceforge.net/crc-catalogue/all.htm
