from django.test import TestCase
import os
from tale import summarizer

class SummarizerTestCase(TestCase):
    def setUp(self):
        self.summarizer = summarizer.Summarizer(None)
    
    # read notes from path
    def test_read_notes(self):
        path = os.path.join(os.path.dirname(__file__), "test_data", "test_texts")
        notes = self.summarizer.readNotesFromPath(path)
        self.assertEqual(len(notes), 2)
        
    # read notes from empty path
    def test_read_notes_empty(self):
        path = os.path.join(os.path.dirname(__file__), "test_data", "test_texts_empty")
        notes = self.summarizer.readNotesFromPath(path)
        self.assertEqual(len(notes), 0)
        
    # def read notes single file
    def test_read_notes_single_file(self):
        path = os.path.join(os.path.dirname(__file__), "test_data", "test_texts", "test1.txt")
        notes = self.summarizer.readNotesFromPath(path)
        self.assertEqual(len(notes), 1)
        
    
    
    # teardown
    def tearDown(self):
        pass