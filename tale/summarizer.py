import os 
import openai
from openai import OpenAI
from pre_processor import PreProcessor
from tqdm import tqdm
import json

class Summarizer:
    """This class contains functions to summarize notes into prompts"""

    def __init__(self):
        """This function initializes the class"""
        # initialize the class
        self.client = None
        self.init_openai()
        return

    def init_openai(self):
        """This function initializes the openai client"""
        # get the openai api key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()
        return
    
    def readNotesFromPath(self, path):
        texts = []
        # read all .txt files from the path
        for file in os.listdir(path):
            if file.endswith(".txt"):
                with open(os.path.join(path, file), "r", encoding="utf8") as f:
                    texts.append(f.read())
        return texts
    
    
    def summarize(self, text):
        """This function takes a string as input and returns a string as output"""
        
        system = """You are a tabletop roleplaying notes summarizer. You are given a set of notes and you have to summarize them into a single string. Try to be specific about timelines and events as well as places and people. 
        Try to give a long response to make sure that you get every detail right and nothing is missing."""
        user = text
        # summarize the text
        response = self.sendPromptToGPT(system=system, user=user, temperature=0.5, model="gpt-3.5-turbo", top_p=0.4)
        
        return response
    
    def preSummary(self, texts):
        """This function takes a list of notes as input and returns a single string as output"""
        # create a single string
        summaries = []
        for text in texts:
            summaries.append(self.summarize(text))
        return summaries
    
    def summarizePreSummaries(self, summaries):
        """This function takes a list of summaries as input and returns a single string as output"""
        model_input = ""
        # summarize the text
        for s in summaries:
            model_input +="NOTE \n\n"
            model_input += s
        
        prompt = """You are a summarization engine which is given a multitude of texts. 
        
        These texts are summaries of notes from different players in a tabletop roleplayin game. 
        All the summaries are about the same game but from different perspectives. Notes of different players are consecutive in the text. Therefore you have to match the same events, people and places in the different summaries.
        Create a single summary of all the notes. Try to be specific about timelines and events as well as places and people. Try to give a long response to make sure that you get every detail right and nothing is missing.
        Also make sure that you create a timeline of events. The timeline should be chronological and match between the different notes and should not contain any contradictions.
        Notes of different Players are seperated by 
        
        NOTE. \n\n"""
        
        response = self.sendPromptToGPT(system=prompt, user=model_input, temperature=0.5, model="gpt-3.5-turbo", top_p=0.4)

        return response
    
    
    def createPromptFromSummaries(self, summary):

        # Reminder: When prompting use the RTFC (Role, Task, Format, Constraint) format for best results. To ensure that the output is more reliable, do not use as high of a temperature as you would for other tasks.
        prompt = """You are a prompt generation machine for image generation. 
        
        Summarize the given story into a set of prompts which can be used to generate images. And output those prompts in a json file.
        
        The format of the json file should be as follows:

            {
            "1": "DESCRIPTION OF SCENE 1 + ART DIRECTION",
            "2" : "DESCRIPTION OF SCENE 2 + ART DIRECTION",
            ...
            }

            A more concrete example would look like this:

            {
            "1": "Two men, both equipped with ornate sword and shield, face each other in a big Colosseum + realistic, bright colors, hd, light mood",
            "2" : "One man equipped with ornate sword and shield and covered in mud is standing over another defeated man. + realistic, bright colors, hd, light mood",
            ...
            }

            Do not be dramatic and only use words which a spectator would use to describe the scene to a computer program.
            
            Use a minimun of 100 words per prompt. 

            Use words like "HD" and "hyperrealistic" in your art direction to ensure a crisp image. Do not repeat descriptions from the scene in the ARE DIRECTION. 
            The ART DIRECTION should only contain direction for mood, coloring and drawing of the image.
            
            Do no use the " character in your prompt since it will break the json file.
            
            Create a maxmimum of 5 prompts. Do not exceed this limit but also do create less then 5 prompts.
            """
        
        response = self.sendPromptToGPT(system=prompt, user=summary, temperature=0.5, model="gpt-3.5-turbo", top_p=0.4)

        return response
    
    def sendPromptToGPT(self, system, user, temperature=1, model="gpt-3.5-turbo", top_p=1):        
        response = self.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
             ],
        temperature=temperature,
        top_p=top_p
        )
        return response.choices[0].message.content
    
    
    def cleanPrompt(self, prompt):
        """This function takes a string as input and returns a string as output"""
        # load context.json
        processor = PreProcessor()
        context = processor.load_json("data//dummy//input//context.json")
        
        # clean the prompt by substituting names which are keys in context.json with their values
        for key in context:
            prompt = prompt.replace(key, context[key])
        
        return prompt
    
    
    def indexNotes(self, story, prompts):
        system = """
            You are a prompt insertion machine.
            You are given two inputs:
            A story and a number of image creation prompts. Prompts are numbered and can be identified with their respective number.
            Insert the prompt numbers at the correct positions of the story where they would fit as descriptions.
            The story starts with the word STORY and the prompts start with the word PROMPTS.
            
            Use each prompt only once and in order of their number.
            
            If you would get an input like this: 
            
            "STORY: Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.   
                    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. 
                    At vero eos et accusam et justo duo dolores et ea rebum.  Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            PROMPTS:
            {
            "1": "DESCRIPTION OF SCENE 1 + ART DIRECTION",
            "2" : "DESCRIPTION OF SCENE 2 + ART DIRECTION",
            }
            
            The output should be a single string which contains the WHOLE story with the prompts inserted at the correct positions like this:
            
            "
            
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. 
            
            (1)
            
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. 
            
            (2)
            
            At vero eos et accusam et justo duo dolores et ea rebum.  Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            
            "
            
            Do not change any of the input texts but only move around positions. Only insert the number and not the full prompt by saying (number of prompt).
            Use all prompts exactly once. Do not leave any prompts out. Do not shorten or lengthen the texts and do not add any additional text. 
            Represent the prompts onlny through numbers in brackets. Do not use any other characters in the brackets.
            Do not include the word PROMPTS or STORY in the output.
        """
        user = "STORY: \n\n" + story + "\n\n PROMPTS: \n\n" + prompts
        response = self.sendPromptToGPT(system=system, user=user, temperature=0.3, top_p=0.2)
        return response
        
        

    def getPropmtsFromNotes(self, path):
        """This function takes a path as input and returns a list of prompts as output"""
        # create a list of prompts
        prompts = []
        with tqdm(total=5) as pbar:
            pbar.set_description("Loading notes...")
            notes = self.readNotesFromPath(path)
            pbar.update(1)
            
            pbar.set_description("Summarizing notes...")
            pre_summary = self.preSummary(notes)
            pbar.update(1)

            pbar.set_description("Summarizing summaries...")
            summary = self.summarizePreSummaries(pre_summary)
            pbar.update(1)
            
            pbar.set_description("Creating prompts...")
            prompts = self.createPromptFromSummaries(summary)
            pbar.update(1)
            
            pbar.set_description("Finding prompt positions...")
            indexedNotes = self.indexNotes(summary, prompts)
            pbar.update(1)            

            pbar.set_description("Cleaning prompts...")
            prompts = self.cleanPrompt(prompts)
            pbar.update(1)
            
        return prompts, indexedNotes
    
    
if __name__ == "__main__":
    summarizer = Summarizer()
    notes = summarizer.readNotesFromPath("data//dummy//input//the_sprawl//")

    pre_summary = summarizer.preSummary(notes)
    summary = summarizer.summarizePreSummaries(pre_summary)
    prompts = summarizer.createPromptFromSummaries(summary)
    
    print(prompts)
    