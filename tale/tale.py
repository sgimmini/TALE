from text2image import Text2Image
from summarizer import Summarizer
from post_processor import PostProcessor
from tqdm import tqdm


# main function
if __name__ == "__main__":
  
    with tqdm(total=5) as pbar:
      
      pbar.set_description("Initalizing...")
      # create an instance of the class
      text2image = Text2Image()
      summarizer = Summarizer()
      postProc = PostProcessor()
     
      # get prompts from the notes
      
      prompts, indexedStory = summarizer.getPropmtsFromNotes("data//dummy//input//the_sprawl//")
      # write the prompts to a json file
      f = open("data//dummy//input//gpt_created_prompts.json", "w")
      f.write(prompts)
      f.close()
      
     # read the prompts from a json file
      f = open("data//dummy//input//gpt_created_prompts.json", "r")
      prompts = f.read()
      f.close() 
      
      
      # write the indexed story to a file
      f = open("data//dummy//input//indexed_story.txt", "w")
      f.write(indexedStory)
      f.close()
      
      
      # read the indexed story from a file
      f = open("data//dummy//input//indexed_story.txt", "r")
      indexedStory = f.read()
      f.close()
      
      
      # generate images from the prompts
      text2image.generateImages("data//dummy//input//gpt_created_prompts.json")
      
      # generate html file from the images
      postProc.process(indexedStory)
    