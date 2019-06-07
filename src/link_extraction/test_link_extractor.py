from unittest import TestCase

from link_extraction import link_extractor

class LinkExtractorTester(TestCase):

    def test_link_extraction(self):

        x = link_extractor.extract_urls_from_text("foo")
        self.assertTrue(x != None)
