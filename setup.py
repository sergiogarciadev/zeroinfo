# -*- coding: utf-8 -*-
"""Python packaging."""

import os
from setuptools import setup, find_packages

from zeroinfo import __version__

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

setup(
    name='zeroinfo',
    version=__version__,
    description='Zero configuration information retriever and service discovery.',
    long_description=open(os.path.join(ROOT_PATH, 'README.md')).read(),
    keywords='zeroconf',
    author='LawfulHacker',
    author_email='lawfulhacker@gmail.com',
    url='https://github.com/LawfulHacker/zeroinfo',
    download_url='https://github.com/LawfulHacker/zeroinfo/releases',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    namespace_packages=[],
    include_package_data=True,
    package_data={},
    zip_safe=False,
    scripts=[],
    entry_points='''
        [console_scripts]
        zeroinfo=zeroinfo.__main__:cli
    ''',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT'
    ],
    install_requires=[
        'click==6.7'
    ],
    tests_require=[
        'pytest'
    ],
    extras_require={
        'dev': [
            'pydocstyle',
            'pylint',
        ]
    },
)
