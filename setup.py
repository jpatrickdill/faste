from setuptools import setup, find_packages
import faste

with open("README.rst", "r") as file:
    long_desc = file.read()

setup(
    name='faste',
    description="dictionary style caches.",
    long_description=long_desc,
    version=faste.__version__,
    url='https://github.com/reshanie/faste',
    license='MIT',
    author='Patrick Dill, a/k/a reshanie',
    author_email='jamespatrickdill@gmail.com',
    install_requires=[],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="cache caches LIFO FIFO RR LRU MRU LFU memory dict dictionary",

    packages=find_packages(exclude=["docs", ".idea"]),
)
