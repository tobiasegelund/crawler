import os
import pytest

from crawler.core.utils.format import *
from crawler.core.utils.system import *


def test_add_http():
    test_url = "//not_here.png"
    assert "http://not_here.png" == add_http(test_url)


def test_extract_file_name():
    test_url = "//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/20px-Semi-protection-shackle.svg.png"
    assert "20px-Semi-protection-shackle.svg.png" == extract_file_name(test_url)
