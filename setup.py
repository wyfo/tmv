from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()

setup(
    name='tmv',
    url="https://github.com/wyfo/tmv",
    author="Joseph Perez",
    author_email="joperez@hotmail.fr",
    description="Type Model Visitor",
    long_description=README,
    long_description_content_type="text/markdown",
    version='0.1.3',
    packages=find_packages(include=["tmv"]),
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
