import unittest

from main import extract_title

class TestBlockTypr(unittest.TestCase):
    def test_extract_title_h1(self):
        md = "### Tolkien\nblah blah\nblah"
        title = extract_title(md)
        self.assertEqual(title, "Tolkien")