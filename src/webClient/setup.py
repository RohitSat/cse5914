#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='webClient',
    version='0.1.0',
    description='Brutus Web Client',
    url='https://github.com/RohitSat/cse5914',

    packages=find_packages(),
    install_requires=[
        'selenium'
    ]
)