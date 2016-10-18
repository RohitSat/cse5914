#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='brutus_module_search',
    version='0.1.0',
    description='Brutus Search Module',
    url='https://github.com/RohitSat/cse5914',

    packages=find_packages(),
    install_requires=[
        'Flask',
        'watson-developer-cloud'
    ],

    entry_points={
        'console_scripts': [
            'brutus_module_search=brutus_module_search.console:main'
        ]
    }
)
