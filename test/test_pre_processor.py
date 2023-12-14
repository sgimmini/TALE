# import django test tools
from django.test import TestCase
import os
from tale import pre_processor
from parameterized import parameterized

# add a test class
class PreProcessorTestCase(TestCase):
    def setUp(self):
        self.pre_processor = pre_processor.PreProcessor()

    # load files from directory
    def test_load_files(self):
        directory = os.path.join(os.path.dirname(__file__), "test_data", "test_texts")
        files = self.pre_processor.load_files(directory)
        self.assertEqual(len(files), 2)
        
    # parse textfile
    def test_load_data(self):
        filepath = os.path.join(os.path.dirname(__file__), "test_data", "test_texts")
        text = self.pre_processor.load_data(filepath)
        self.assertEqual(text, "abcd1234")
        
    # def parse textfile
    def test_parse_textfile(self):
        filepath = os.path.join(os.path.dirname(__file__), "test_data", "test_texts", "test1.txt")
        text = self.pre_processor.parse_textfile(filepath)
        self.assertEqual(text, "abcd")
        
    # def parse textfile wrong file
    def test_parse_textfile_wrong_file(self):
        filepath = os.path.join(os.path.dirname(__file__), "test_data", "test_texts", "test.yaml")
        with self.assertRaises(ValueError):
            self.pre_processor.parse_textfile(filepath)
            
    # def load json
    def test_load_json(self):
        filepath = os.path.join(os.path.dirname(__file__), "test_data", "test_texts", "test.json")
        text = self.pre_processor.load_json(filepath)
        self.assertEqual(text["test"], "123")
        
    # parametrize test_write_file to test_data/test_write.txt
    @parameterized.expand([
        ("", os.path.join(os.path.dirname(__file__), "test_data", "test_write.txt")),
        ("abcd", os.path.join(os.path.dirname(__file__), "test_data", "test_write.txt"))
    ])
    
    def test_write_file(self, data, filepath):
        self.pre_processor.write_file(data, filepath=filepath)
        with open(filepath, "r", encoding="UTF-8") as file:
            text = file.read()
            self.assertEqual(text, data)
    
    # clean up test_write.txt
    def tearDown(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), "test_data", "test_write.txt")):
            os.remove(os.path.join(os.path.dirname(__file__), "test_data", "test_write.txt"))
        
        