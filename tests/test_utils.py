import os
from pathlib import Path

from crawler.utils.format import *
from crawler.utils.system import *


def test_add_http_if_missing():
    test_url = "//not_here.png"
    assert "http://not_here.png" == add_http_if_missing(test_url)


def test_extract_file_name_url():
    test_url = "//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/20px-Semi-protection-shackle.svg.png"
    assert "20px-Semi-protection-shackle.svg.png" == extract_file_name_url(test_url)


def test_create_dir_if_not_exits():
    dir_name = Path("test_folder")
    create_dir_if_not_exits(dir_name)
    assert dir_name.exists()


def test_remove_dir_if_exists():
    dir_name = Path("test_folder")
    remove_dir_if_exists(dir_name)


def test_get_domain():
    url = "https://en.wikipedia.org/wiki/Manchester_United_F.C."
    domain = get_hostname(url)
    assert domain == "en.wikipedia.org"
