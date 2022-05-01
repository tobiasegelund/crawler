## Crawler

A CLI program to download image, video or audio files from a website url. The program
offers the option to crawl deeper within the domain, but only of the specified domain. Furhermore,
the program offers the option to render the website in order to capture javascript related
content with the expense of increase in the crawling speed.

Currently, the program is a beta version and cannot capture all possible scenerios.

### Download
```console
git clone git@github.com:tobiasegelund/crawler.git
```

### Install
```console
make install
```
Installation within a virtual environment 
```console
python3 -m venv env
source env/bin/activate
pip install -r requirements/base.txt
```

### Usage
```console
crawler [image, video, audio] --url https://www.dr.dk
```

### Help
Please take a look in the help section to view possible options.
```console
crawler [image, video, audio] --help
```
