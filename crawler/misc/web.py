from urllib.parse import urlparse


class Website:
    def __init__(self, url: str) -> None:
        self._url = url
        self._parsed_url = urlparse(url)

    @property
    def url(self) -> str:
        return self._url

    @property
    def scheme(self) -> str:
        return self._parsed_url.scheme

    @property
    def domain(self) -> str:
        return self._parsed_url.hostname

    @property
    def netloc(self) -> str:
        return (
            self._parsed_url.netloc[4:]
            if self._parsed_url.netloc[:4] == "www."
            else self._parsed_url.netloc
        )

    @property
    def link(self) -> str:
        return self.scheme + "://" + self.domain
