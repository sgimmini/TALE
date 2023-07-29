"""
Pre processing module for preparing data for models pipeline.

"""

from pydantic import BaseModel

class PreProcessor(BaseModel):
    """
    Pre processing class for preparing data for models pipeline.

    """

    def format(self, full_text: str) -> str:
        """
        Format text for models pipeline.

        :param full_text: text to be formatted
        :return: formatted text
        """
        raise NotImplementedError

    def merge_files(self, files: list) -> str:
        """
        Merge list of files into one string.

        :param files: list of files
        :return: merged string; full text
        """
        raise NotImplementedError

    def parse_textfile(self, file: str) -> str:
        """
        Parse file into string.

        :param file: path to file to be parsed
        :return: parsed string; full text
        """
        raise NotImplementedError


    def load_files(self, directory: str) -> list:
        """
        Load files from directory.

        :param directory: path to directory
        :return: list of files
        """
        raise NotImplementedError
