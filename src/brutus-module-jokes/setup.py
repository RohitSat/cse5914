#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='brutus_module_jokes',
    version='0.1.0',
    description='Brutus Jokes Module',
    url='https://github.com/RohitSat/cse5914',

    packages=find_packages(),
    install_requires=[
        'Flask'
        'watson-developer-cloud'
    ],

    entry_points={
        'console_scripts': [
            'brutus_module_jokes=brutus_module_jokes.console:main'
        ]
    }
)
