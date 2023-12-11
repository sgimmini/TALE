from django.test import TestCase
import os
from tale import summarizer

class SummarizerTestCase(TestCase):
    def setUp(self):
        self.summarizer = summarizer.Summarizer()
    
    # read notes from path
    def test_read_notes(self):
        path = os.path.join(os.path.dirname(__file__), "test_data", "test_texts")
        notes = self.summarizer.read_notes(path)
        self.assertEqual(len(notes), 2)
        
    # read notes from empty path
    def test_read_notes_empty(self):
        path = os.path.join(os.path.dirname(__file__), "test_data", "test_texts_empty")
        notes = self.summarizer.read_notes(path)
        self.assertEqual(len(notes), 0)
    
    # teardown
    def tearDown(self):
        pass