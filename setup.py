import os

from setuptools import setup, find_packages

import faste

on_rtd = os.getenv('READTHEDOCS') == 'True'

with open("README.rst", "r") as file:
    long_desc = file.read()

requires = []
if on_rtd:
    requires.append("sphinxcontrib")

setup(
    name='faste',
    description="dictionary style caches.",
    long_description=long_desc,
    version=faste.__version__,
    url='https://github.com/reshanie/faste',
    license='MIT',
    author='Patrick Dill',
    author_email='jamespatrickdill@gmail.com',
    install_requires=requires,
    download_url="http://github.com/reshanie/faste/archive/master.tar.gz",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="faste cache caches LIFO FIFO RR LRU MRU LFU memory dict dictionary",

    packages=find_packages(exclude=["docs", ".idea"]),
)
