#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from setuptools import setup, find_packages
from codecs import open

requires = [
    'click',
    'cookiecutter',
    'networkx',
    'numpy',
    'pandas',
    'tornado',
    'tqdm',
    'mesa'
]

extras_require = {
    'dev': [
        'coverage',
        'flake8',
        'pytest >= 3.6',
        'pytest-cov',
        'sphinx',
    ],
    'docs': [
        'sphinx',
    ]
}

version = ''
with open('apocalypse_sim/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name='Mesa',
    version=version,
    description="Agent-based modeling (ABM) in Python 3+",
    author='Project Mesa Team',
    author_email='projectmesa@googlegroups.com',
    url='https://github.com/PimPaardekooper/zombie_apocalypse',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    extras_require=extras_require,
    keywords='agent based modeling model ABM simulation multi-agent',
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Life',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
    ],
    entry_points='''
        [console_scripts]
        mesa=mesa.main:cli
    ''',
)