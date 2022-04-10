## Crawler

A CLI program to download images, videos or audio files from a website link. The program
offers the option to crawl deeper within the domain, but only of the specified domain. Furhermore,
the program offers to the option to render the website in order to capture javascript related
content, but it does increase the speed of scraping.

Currently, the program a beta version and capture all possible scenerios. Thus, bare with
issues to some websites.

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