#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
execfile('ubuntufinder/version.py') # Load version

setup(
    name='ubuntufinder',
    version=__version__,
    description='An utility package to locate the latest Ubuntu AMIs.',
    long_description=readme + '\n\n' + history,
    author='Thomas Orozco',
    author_email='thomas@orozco.fr',
    url='https://github.com/krallin/ubuntufinder',
    packages=[
        'ubuntufinder',
    ],
    package_dir={'ubuntufinder': 'ubuntufinder'},
    entry_points={
        'console_scripts': [
            'ubuntufinder = ubuntufinder.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    license='BSD',
    zip_safe=False,
    keywords='ubuntufinder',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
