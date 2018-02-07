crc
====

The crc module provides classes to easily implement and calculate arbitrary crc algorithms CRC-8, 16, 24, 32.
It also commes with 3 handy tools:

* **crc-table** which can be used to generate a crc table for a specific crc algorithm/polynom.
* **crc** 

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

The crc module provides provides functionality to handle and calculate various kinds of crc checksums.
(e.g. Crc8, Crc16, Crc32)

Links
-----
* `A Painless guide to crc error detection algorithms <http://www.zlib.net/crc_v3.txt>`_
* `Project on Github <https://github.com/Nicoretti/crc>`_

Requirements
------------
* Python 3.5 and newer

Installation
------------

TBD

Usage
------

.. code-block::

    data = b"foo bar need crc"
    crc8.CCITT

