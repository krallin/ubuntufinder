=====
Usage
=====

Installation
************

Use ``pip``:

::

    $ pip install --upgrade ubuntufinder

CLI Usage
*********

::

    $ ubuntufinder -r precise -a amd64 -i ebs -v paravirtual us-east-1
    ami-fa7dba92

Run ``ubuntufinder -h`` for usage information.


Quickstart
**********

::

    >>> import ubuntufinder
    >>> ubuntufinder.find_image("us-east-1")
    <Image: raring@us-east-1: 2013-08-24 00:00:00 (amd64 ebs paravirtual)>
    >>> image = ubuntufinder.find_image("us-west-1", "precise", "amd64", "ebs", "paravirtual")
    >>> image.ami_id
    'ami-c4072e81'


Advanced Usage
**************

``find_image`` uses sane defaults, but accepts extra arguments that let you customize your search.

.. autofunction:: ubuntufinder.find_image
