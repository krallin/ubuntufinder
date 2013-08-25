========
Usage
========

The main entry point to Ubuntu Finder is :func:`ubuntufinder.find_image`.

Quickstart
**********

::

    >>> import ubuntufinder
    >>> ubuntufinder.find_image("us-east-1")
    <Image: raring@us-east-1: 2013-08-24 00:00:00 (amd64 ebs paravirtual)>


Advanced Usage
**************

``find_image`` uses sane defaults, but accepts extra arguments that let you customize your search.

.. autofunction:: ubuntufinder.find_image
