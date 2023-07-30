import unittest
import sys
sys.path.append('../..')
from source.pre_processor import PreProcessor

class TestPreProcessor(unittest.TestCase):
    """Testing the PreProcessor class"""

    def setUp(self) -> None:
        self.filepath = 'consumerfiles/test.txt'
        self.directory = 'consumerfiles'
        self.preprocessor = PreProcessor()

    def test_readin(self):
        # Act

        read_in = self.preprocessor.parse_textfile(self.filepath)

        #Assert

        self.assertIsInstance(read_in, str)
    
    def test_read_directory(self):
        # ActP
        read_in = self.preprocessor.parse_textfolder(self.directory)

        self.assertIsInstance(read_in, str)
