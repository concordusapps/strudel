#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from imp import load_source
import sys


setup(
    name='strudel',
    version=load_source('', 'strudel/_version.py').__version__,
    description='A Python 3 Vcard parser.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    author='Concordus Applications',
    author_email='support@concordusapps.com',
    url='http://github.com/concordusapps/strudel',
    packages=find_packages('.'),
    install_requires=[],
)
