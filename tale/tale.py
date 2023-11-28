from text2image import Text2Image
from summarizer import Summarizer
from post_processor import PostProcessor



# main function
if __name__ == "__main__":
    # create an instance of the class
    text2image = Text2Image()
    summarizer = Summarizer()
  #  postProc = PostProcessor()
    
    # get prompts from the notes
    prompts = summarizer.getPropmtsFromNotes("data//dummy//input//the_sprawl//")
    # write the prompts to a json file
    f = open("data//dummy//input//gpt_created_prompts.json", "w")
    f.write(prompts)
    f.close()

    # generate images from the prompts
    text2image.generateImages("data//dummy//input//gpt_created_prompts.json")
    
    # generate html file from the images
 #   postProc.generateHtmlFile()
    