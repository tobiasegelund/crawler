from setuptools import setup, find_packages
from crawler import VERSION

# with open("requirements/base.txt") as f:
#     required = f.read().splitlines()

setup(
    name="crawler",
    version=VERSION,
    author="Tobias Egelund",
    packages=find_packages(exclude=["tests*"]),
    description="""
    A micro crawl tool to scrape audio, video and image files from websites
    """,
    classifiers = """
        Environment :: Web Environment
        Framework :: Crawler
        Intended Audience :: Developers
        Operating System :: OS Independent
        Programming Language :: Python :: 3.8
        Programming Language :: Python :: 3.9
        Topic ::Web Crawl :: Web Scrape :: Application Frameworks
    """,
    install_requires=[
        "bs4>=0.0.1",
        "requests>=2.27.1",
        "requests-html>=0.10.0",
        "tqdm>=4.63.0",
        "click>=8.0",
        "python-dotenv>=0.19.2",
        "nest-asyncio>=1.5.4",
    ],
    entry_points={
        "console_scripts": [
            "crawler=crawler.cli:main",
        ],
    },
    python_requires=">=3.8",
)
