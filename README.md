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

### Build
```console
make install
```

### Usage
```console
crawler [image, video, audio] --url https://www.dr.dk
```
Or
```console
python3 crawler [image, video, audio] --url https://www.dr.dk
```