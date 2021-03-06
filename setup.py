import os

from setuptools import setup


def getdes():
    des = ""
    if os.path.isfile(os.path.join(os.getcwd(), "README.md")):
        with open(os.path.join(os.getcwd(), "README.md")) as fi:
            des = fi.read()
    return des


def get_version():
    v = {}
    with open("src/version.py") as fi:
        c = fi.read()
    exec(compile(c, "src/version.py", "exec"), v)
    return v["__version__"]


setup(
    name="ezmonitor",
    version=get_version(),
    packages=["ezmonitor"],
    package_dir={"ezmonitor": "src"},
    author_email="yodeng@tju.edu.cn",
    url="https://github.com/yodeng/ezmonitor",
    install_requires=["matplotlib", "psutil", "pandas", "numpy"],
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
