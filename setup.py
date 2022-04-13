import os
import sys
import site
import sysconfig
import subprocess

from setuptools import setup
from src.version import __version__


def getdes():
    des = ""
    if os.path.isfile(os.path.join(os.getcwd(), "README.md")):
        with open(os.path.join(os.getcwd(), "README.md")) as fi:
            des = fi.read()
    return des


setup(
    name="ezmonitor",
    version=__version__,
    packages=["ezmonitor"],
    package_dir={"ezmonitor": "src"},
    author_email="yodeng@tju.edu.cn",
    url="https://github.com/yodeng/ezmonitor",
    install_requires=["matplotlib", "psutil", "pandas"],
    python_requires='>=2.7.10, <3.10',
    long_description=getdes(),
    long_description_content_type='text/markdown',
    license="BSD",
    entry_points={
        'console_scripts': [
            'ezmntor = ezmonitor.main:main',
        ]
    }
)
