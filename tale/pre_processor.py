"""
Pre processing module for preparing data for models pipeline.

"""

import os
from pydantic import BaseModel
import json

class PreProcessor(BaseModel):
    """
    Pre processing class for preparing data for models pipeline.

    """

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

    def load_data(self, filepath: str) -> str:
        """
        Loads txt's from filepath and returns a string of all the text.
        """
        files = self.load_files(filepath)
        merged_text = ''
        for f in files:
            merged_text = merged_text + self.parse_textfile(f)
        return merged_text

    def load_json(self, filepath: str) -> dict:
        """
        Loads json from filepath.
        """
        if not filepath.endswith(".json"):
            raise ValueError("File must be a .json file.")

       # load json file
        with open(filepath, 'r', encoding="UTF-8") as json_file:
            output = json.load(json_file)

        return output