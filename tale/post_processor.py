from bs4 import BeautifulSoup
import os
import re 
from tqdm import tqdm
class PostProcessor:
    """
    The class which processes the content generated by the Summarizer class.
    Attributes:
        content (Content) : The content to be processed
    """

    def __init__(self):
        return

            
    def generateHtml(self, indexedStory):
        """
        Generates a html string from the content.
        Returns:
            html (str) : The html string
        """
        # read html structure from html file
        dummy_html = open('.//data//dummy//website//dummy.html', 'r').read()
        # read corresponding css file
        dummy_css = open('.//data//dummy//website//dummy.css', 'r').read()

        # create a beautiful soup object
        soup = BeautifulSoup(dummy_html, 'html.parser')

        # set the title
        soup.title.string = "We are still testing"

        # add css to the html file
        head = soup.find('head')
        head.append(soup.new_tag('style', type='text/css'))
        head.style.append(dummy_css)

        # open path to images
        path = 'C://Users//fraul//Documents//GitHub//TALE//data//dummy//output'
        print(re.findall(r"\((100|[1-9]?\d)\)", indexedStory))
        # using regular expressions find all occurences of (NUMERIC) in indexed story, add the part of the story before the occurence to the html file, add the image to the html file
        for i in tqdm(re.findall(r'\(\d+\)', indexedStory), desc="Generating HTML..."):
            # find the index of the occurence
            index = indexedStory.index(i)
            # create a new section with class "content-block"
            new_section = soup.new_tag('section')
            new_section['class'] = 'content-block'
            # add a image to the section
            new_img = soup.new_tag('img')
            new_img['src'] = path + "//" + str(i[1]) + ".png"
            new_section.append(new_img)
            # add a paragraph to the section
            new_p = soup.new_tag('p')
            new_p.string = indexedStory[:index]
            
            # add the section to the html file
            new_section.append(new_p)
            # add the section to the html file body
            soup.body.append(new_section)

        return soup.prettify()
    
    def writeHtml(self, path, html):
        """
        Writes the html string into a file.
        Attributes:
            path (str) : The path to the file
            html (str) : The html string
        """
        # write the html string into a file
        open(path, 'w', encoding='utf-8').write(html)
        return
    
    def process(self, indexedStory):
        """
        Processes the content by generating a html and writing it into a file.
        """
        html = self.generateHtml(indexedStory)
        self.writeHtml("data//dummy//output//" + 'output.html', html)
        return


# create a main function in order to test the class
def __main__():
    return

# call the main function
if __name__ == '__main__':
    __main__()