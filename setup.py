import setuptools
from setuptools import setup

setup(
    name="kissom",
    version="1.3.1",
    author="Joe Marchionna",
    author_email="joemarchionna@gmail.com",
    description="Keep It Simple Stupid Object Manager",
    long_description=open("readme.md").read(),
    license=open("license.md").read(),
    packages=setuptools.find_packages(),
    url="https://github.com/joemarchionna/kissom.git",
    keywords=["ORM", "DATA ACCESS"],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
