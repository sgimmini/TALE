import json

class Content:
    """
    The class which stores the structure of generated content for later consumption.

    Attributes:
        title (str) : The title of the summarized content
        text (list(str)) : A list of texts which represent the body of the summary
        images (list(str)) : A list of references to images
    """
    title = ''
    text = ['']
    images = ['']


    def __init__(self, title, text, images):
        """
        The constructor for the Content class.
        Attributes:
            title (str) : The title of the summarized content
            text (list(str)) : A list of texts which represent the body of the summary
            images (list(str)) : A list of references to images
        """
        self.title = title
        self.text = text
        self.images = images
        return
    
    
    def loadFile(self, path):
        """
        Loads itself through a json file.
        Attributes:
            path (str) : The path to the json file
        """
        # load the variables of this class from a json file
        jsonstring = open(path, 'r').read()
        fileContent = json.loads(jsonstring, strict=False)
        self.title = fileContent['title']
        self.text = fileContent['text']
        self.images = fileContent['images']
        return

    def dumpFile(self, path):
        """
        Dumps itself to a json file.
        Attributes:
            path (str) : The path to the json file
        """
        # write the variables of this class to a json file
        fileContent = {
            'title': self.title,
            'text': self.text,
            'images': self.images
        }
        json.dump(fileContent, open(path, 'w'))
        return
