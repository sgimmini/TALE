from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os

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
        dummy_html = open(os.path.join(os.path.dirname(__file__),"..", "media", "website", "template.html"), "r").read()
        # read corresponding css file
        dummy_css = open(os.path.join(os.path.dirname(__file__),"..", "media", "website", "template.css"), "r").read()

        # create a beautiful soup object
        soup = BeautifulSoup(dummy_html, "html.parser")

        # set the title
        soup.title.string = "TALE"

        # add css to the html file
        head = soup.find("head")
        head.append(soup.new_tag("style", type="text/css"))
        head.style.append(dummy_css)

        # Find the placeholder div where new content will be added
        new_content_div = soup.find("div", id="new-content")

        # regex
        regex = re.findall(r"\(\d+\)", indexedStory)

        last_index = 0
        # using regular expressions find all occurences of (NUMERIC) in indexed story,
        # add the part of the story before the occurence to the html file, add the image to the html file
        for i in tqdm(range(len(regex)), desc="Generating HTML..."):
            # find the index of the occurence
            index = indexedStory.index(regex[i])

            # Create a new 'div' for the content block
            new_block = soup.new_tag(
                "div", attrs={"class": "content-block", "id": f"block{i}"}
            )

            # Add an additional class for skew direction
            skew_class = "skew-left" if i % 2 == 0 else "skew-right"
            new_block["class"] = new_block.get("class", []) + [skew_class]

            # Set the inline background image style for the new content block
            new_block_style = f"""
                background: url('{regex[i][1] + ".png"}') no-repeat center center;
                background-size: cover;
                """
            new_block["style"] = new_block_style.strip()

            # Create a new 'div' for text content
            text_content = soup.new_tag("div", attrs={"class": "text-content"})
            new_block.append(text_content)

            # Create and append a new 'h2' tag to the text content
            header = soup.new_tag("h2")
            header.string = ""
            text_content.append(header)

            # Create and append a new 'p' tag to the text content
            paragraph = soup.new_tag("p")
            paragraph.string = indexedStory[last_index:index]

            # if the index is not the last index of the list add also the part of the story after the occurence to the html file
            if i == len(regex) - 1:
                paragraph.string += indexedStory[index:]

            # remove from paragraph string any occurence of (NUMERIC)
            remove_regex = re.findall(r"\(\d+\)", paragraph.string)
            for i in range(len(remove_regex)):
                paragraph.string = paragraph.string.replace(remove_regex[i], "")

            text_content.append(paragraph)
            # Insert the new content block into the placeholder div
            new_content_div.append(new_block)

            last_index = index

        new_content_div.unwrap()
        return soup.prettify()

    def writeHtml(self, path, html):
        """
        Writes the html string into a file.
        Attributes:
            path (str) : The path to the file
            html (str) : The html string
        """
        # write the html string into a file
        open(path, "w", encoding="utf-8").write(html)
        return

    def process(self, indexedStory, outPath):
        """
        Processes the content by generating a html and writing it into a file.
        """
        html = self.generateHtml(indexedStory)
        self.writeHtml(os.path.join(os.path.dirname(__file__),".", "media", "outputs", outPath, "output.html"), html)
        return


# create a main function in order to test the class
def __main__():
    return


# call the main function
if __name__ == "__main__":
    __main__()
