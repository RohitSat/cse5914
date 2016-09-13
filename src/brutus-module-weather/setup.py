#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='brutus_module_weather',
    version='0.1.0',
    description='Brutus Weather Module',
    url='https://github.com/RohitSat/cse5914',

    packages=find_packages(),
    install_requires=[
        'Flask'
    ],

    entry_points={
        'console_scripts': [
            'brutus_module_weather=brutus_module_weather.console:main'
        ]
    }
)
