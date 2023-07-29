"""
Pre processing module for preparing data for models pipeline.

"""

import os
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

    def merge_files(self, files: list[str]) -> str:
        """
        Merge list of files into one string.

        :param files: list of files
        :return: merged string; full text
        """
        raise NotImplementedError


    def parse_textfile(self, filepath: str) -> str:
        """
        Parse file into string.

        :param file: path to file to be parsed
        :return: parsed string; full text
        """
        def clean_text(text:str) -> str:
            """
            Remove not needed characters from text.
            Like newlines, tabs, etc.

            """
            text = text.replace('\n', '').replace('\r', '')\
                .replace('\t', '').replace('\f', '').replace('\v', '')
            return text


        if not filepath.endswith(".txt"):
            raise ValueError("File must be a .txt file.")

        with open(filepath, 'r', encoding="UTF-8") as file:
            # read file into string
            full_text = file.read()
            # remove newlines
            full_text = clean_text(full_text)

        return full_text



    def parse_textfolder(self, filepath: str) -> str:
        """
        Parse file into string.

        :param file: path to folder to be parsed
        :return: parsed string; full text of all files concatinated
        """
        files = self.load_files(filepath)
        return self.concatinate_files(files=files)
    

    def load_files(self, directory: str) -> list[str]:
        """
        Load files from directory.

        :param directory: path to directory
        :return: list of files
        """
        files = os.listdir(directory)
        txt_files  = []
        for filename in files:
            if filename.endswith('.txt'):
                txt_files.append(directory+ '/' + filename)

        return txt_files
    def concatinate_files(self, files: list[str]) -> str:
        """Concatinates the input of a list of filepaths"""

        merged_text = ''
        for file in files:
            merged_text = merged_text + self.parse_textfile(file)
        return merged_text
