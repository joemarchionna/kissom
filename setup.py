import setuptools, json
from setuptools import setup

_metadata = json.load(open("versions/_metadata.json", "r"))

setup(
    name=_metadata["name"],
    version=_metadata["version"],
    author=_metadata["author"],
    author_email=_metadata["author_email"],
    description=_metadata["description"],
    long_description=open("readme.md").read(),
    license=open("license.md").read(),
    package_data={"kissom": ["*.json"]},
    include_package_data=True,
    packages=setuptools.find_packages(),
    url=_metadata["url"],
    keywords=["ORM", "DATA ACCESS"],
    install_requires=open("requirements/prod.txt", "r").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
