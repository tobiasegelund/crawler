from pathlib import Path

from crawler.utils.format import *
from crawler.utils.system import *
from crawler.utils.web import *


def test_add_http_if_missing():
    test_url = "//not_here.png"
    assert "http://not_here.png" == add_http_if_missing(test_url, scheme="http")


def test_get_filename():
    test_url = "//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/20px-Semi-protection-shackle.svg.png"
    assert "20px-Semi-protection-shackle.svg.png" == get_filename(test_url)
