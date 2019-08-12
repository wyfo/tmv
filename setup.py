from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()

setup(
    name='TMV',
    url="https://github.com/wyfo/apischema",
    author="Joseph Perez",
    author_email="joperez@hotmail.fr",
    description="Type Model Visitor",
    long_description=README,
    long_description_content_type="text/markdown",
    version='0.1.0',
    packages=find_packages(include=["src"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)
