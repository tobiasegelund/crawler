from setuptools import setup, find_packages
from crawler import VERSION

with open("requirements/base.txt") as f:
    required = f.read().splitlines()

setup(
    name="crawler",
    version=VERSION,
    author="Tobias Egelund",
    packages=find_packages(exclude=["tests*"]),
    description="""
    A CLI program to crawl and scrape websites for scpecific types
    of files, i.e. images, videos or audio files
    """,
    install_requires=required,
    entry_points={
        "console_scripts": [
            "crawler=crawler.cli:main",
        ],
    },
    python_requires=">=3.8",
)
