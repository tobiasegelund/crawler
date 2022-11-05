# Crawler
A CLI program to download image, video or audio files from a website url. The program
offers the option to crawl deeper within the domain, but only of the specified domain. Furhermore,
the program offers the option to render the website in order to capture javascript related
content with the expense of increase in speed.

Currently, the program is a beta version and cannot capture all possible scenerios.

## Install
```console
pip install git+https://github.com/tobiasegelund/crawler.git
```

## Usage
```console
crawler [image, video, audio] --url <URL>
```

### Example
```console
crawler image --url https://www.dr.dk
```

## Help
Please take a look in the help section to view possible options for each command.
```console
crawler [image, video, audio] --help
```
