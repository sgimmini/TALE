from .text2image import Text2Image
from .summarizer import Summarizer, get_new_client
from .post_processor import PostProcessor
import os
import random
from .context_manager import ContextManager

def runPipeline(file : str):
    # create an instance of the class
    text2image = Text2Image()
    summarizer = Summarizer(get_new_client())
    postProc = PostProcessor()

    # create random id
    id = random.randint(0, 1000000000)
    id = str(id)
    
    # create directory for output if not exists
    if not os.path.exists(os.path.join(os.path.dirname(__file__), ".", "media", "outputs", id)):
        os.makedirs(os.path.join(os.path.dirname(__file__), ".", "media", "outputs", id))
    
    # get prompts from the notes
    prompts, indexedStory = summarizer.getPropmtsFromNotes(file)

    # generate images from the prompts
    text2image.generateImages(prompts, id)

    # generate html file from the images
    postProc.process(indexedStory, id)


def runEntityExtraction(file : str):
    # create an instance of the class
    contextManager = ContextManager()

    # read content of file
    with open(file, 'r') as f:
        content = f.read()
    
    # get entities from the notes
    entities = contextManager.get_entities(content)

    # write entities to context.json
    contextManager.write_entities(entities)

# main function
if __name__ == "__main__":
    runPipeline()