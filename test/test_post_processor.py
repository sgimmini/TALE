from django.test import TestCase
import os
from tale import post_processor

class PostProcessorTestCase(TestCase):
    def setUp(self):
        self.post_processor = post_processor.PostProcessor()
    
    # write html
    def test_write_html(self):
        path = os.path.join(os.path.dirname(__file__), "test_data", "test_texts")
        html = "<html><body><p>test</p></body></html>"
        self.post_processor.writeHtml(path, html)
        self.assertEqual(open(path, "r", encoding="utf-8").read(), html)
        
    # teardown
    def tearDown(self):
        path = os.path.join(os.path.dirname(__file__), "test_data", "test_texts")
        os.remove(path)