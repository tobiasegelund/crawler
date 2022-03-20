from tqdm import tqdm
import requests
from .state import State
from crawler.utils.format import add_http, extract_file_name_url
from crawler.config import IMAGE_TYPES, DEBUG_MODE


class Image(State):
    def scan(self) -> None:
        self.img_tags = self.context.html.select("img")

    def filter_on_size(self, width: int = 150, height: int = 150, **kwargs) -> None:
        self.img_tags = list(
            link
            for link in self.img_tags
            if int(link["width"]) >= width and int(link["height"]) >= height
        )

    def filter_on_image_types(self) -> None:
        pass

    def download(self) -> None:
        if not DEBUG_MODE:
            for link in tqdm(self.img_tags):
                url = add_http(link["src"])
                name = extract_file_name_url(url)
                with open(self.context.save_dir.joinpath(name), "wb") as f:
                    f.write(requests.get(url).content)

    def execute(self, **kwargs):
        self.scan()
        self.filter_on_size(**kwargs)
        self.download()
