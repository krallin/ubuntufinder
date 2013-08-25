===============================
Ubuntu AMI Locator
===============================

.. image:: https://badge.fury.io/py/ubuntufinder.png
    :target: http://badge.fury.io/py/ubuntufinder
    
.. image:: https://travis-ci.org/krallin/ubuntufinder.png?branch=master
        :target: https://travis-ci.org/krallin/ubuntufinder

.. image:: https://pypip.in/d/ubuntufinder/badge.png
        :target: https://crate.io/packages/ubuntufinder?version=latest


An utility package to locate the latest Ubuntu AMIs.

* Quickstart: http://ubuntufinder.readthedocs.org/en/latest/usage.html
* Documentation: http://ubuntufinder.readthedocs.org.
* Free software: BSD license


Quickstart
**********

::

    >>> import ubuntufinder
    >>> ubuntufinder.find_image("us-east-1")
    <Image: raring@us-east-1: 2013-08-24 00:00:00 (amd64 ebs paravirtual)>
    >>> image = ubuntufinder.find_image("us-west-1", "precise", "amd64", "ebs", "paravirtual")
    >>> image.ami_id
    'ami-c4072e81'
