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
        # summarize the text
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a tabletop roleplaying notes summarizer. You are given a set of notes and you have to summarize them into a single string. Try to be specific about timelines and events as well as places and people. Try to give a long response to make sure that you get every detail right and nothing is missing."},
            {"role": "user", "content": text},
             ]
        )
        return response.choices[0].message.content
    
    def preSummary(self, texts):
        """This function takes a list of notes as input and returns a single string as output"""
        # create a single string
        summaries = []
        for text in tqdm(texts):
            summaries.append(self.summarize(text))
        return summaries
    
    def summarizePreSummaries(self, summaries):
        """This function takes a list of summaries as input and returns a single string as output"""
        model_input = ""
        # summarize the text
        for s in summaries:
            model_input +="NOTE \n\n"
            model_input += s
        
        prompt = """You are a summarization engine which is given a multitude of texts. These texts are summaries of notes from different players in a tabletop roleplayin game. 
        All the summaries are about the same game but from different perspectives. Notes of different players are consecutive in the text. Therefore you have to match the same events, people and places in the different summaries.
        Create a single summary of all the notes. Try to be specific about timelines and events as well as places and people. Try to give a long response to make sure that you get every detail right and nothing is missing.
        Also make sure that you create a timeline of events. The timeline should be chronological and match between the different notes and should not contain any contradictions.
        Notes of different Players are seperated by NOTE. \n\n"""
        
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": model_input},
             ]
        )
        return response.choices[0].message.content
    
    
    def createPromptFromSummaries(self, summary):

        prompt = """You are a prompt generation machine for image generation. Summarize the given story in as many scenes as needed. Each scene should be told in one prompt.
        Instead of telling the story outright, describe each prompt in detail as if frozen in time. 
        Your output will be used as input for a text-to-image generation model, so ensure that logical constraints are met. 
        Do not describe characters or locations but rather use their names. If you describe only use descriptions from the input.
        Each prompt should be described as a moment in time, so as not to confuse the text-to-image model through changes in places / times.  
        Each prompt must have a minimum number of 100 words. ART DIRECTION is always the exact WORDS in each prompt. Output the story in the following format:

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

            Use words like "HD" and "hyperrealistic" in your art direction to ensure a crisp image. Do not repeat descriptions from the scene in the ARE DIRECTION. 
            The ART DIRECTION should only contain direction for mood, coloring and drawing of the image.
            
            Do no use the " character in your prompt since it will break the json file.
            """
        
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": summary},
             ]
        )
        return response.choices[0].message.content
    
    def sendPromptToGPT(self, system, user):        
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
             ]
        )
        return response.choices[0].message.content
    
    
    def cleanPrompt(self, prompt):
        """This function takes a string as input and returns a string as output"""
        # load context.json
        processor = PreProcessor()
        context = processor.load_json("data//dummy//input//context.json")
        
        # clean the prompt by substituting names which are keys in context.json with their values
        for key in tqdm(context):
            prompt = prompt.replace(key, context[key])
        
        return prompt
    
    
    def indexNotes(self, story, prompts):
        system = """
            You are given two inputs:
            A story and image creation prompts.
            The image creation prompts were created based upon the story. Prompts are numbered and can be identified with their respective number.
            Insert the prompt numbers at the correct positions of the story where they would fit as descriptions.
            Do not change any of the input texts but only move around positions. Only insert the number and not the full prompt by saying INSERT_PROMPT: NUMBER
        """
        user = "STORY: \n\n" + story + "\n\n PROMPTS: \n\n" + prompts
        response = self.sendPromptToGPT(system=system, user=user)
        return response
        
        

    def getPropmtsFromNotes(self, path):
        """This function takes a path as input and returns a list of prompts as output"""
        # create a list of prompts
        prompts = []
        with tqdm(total=6) as pbar:
            pbar.set_description("Loading notes...")
            notes = self.readNotesFromPath(path)
            pbar.update(1)
            
            pbar.set_description("Summarizing notes...")
            pre_summary = self.preSummary(notes)
            pbar.update(1)
            
            pbar.set_description("Summarizing summaries...")
            summary = self.summarizePreSummaries(pre_summary)
            pbar.update(1)
            
            print(summary)
            
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
    