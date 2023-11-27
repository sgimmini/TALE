import os 
import openai
from openai import OpenAI
from pre_processor import PreProcessor


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

        prompt = """You are a prompt generation machine for image generation. Summarize the given story in 7 scenes.  Instead of telling the story outright, describe each scene in detail as if frozen in time. Your output will be used as input for a text-to-image generation model, so ensure that logical constraints are met. For example: Do not use names, but rather describe characters & locations in detail. Focus on detailed descriptions. 
        If you introduce a character, describe them with 3–4 points. If you introduce a place, describe them with 3-4 points. 
        Re-use descriptions if you re-use a location or a character. Each scene should be described as a moment in time, so as not to confuse the text-to-image model through changes in places / times.  
        Each scene must have a MAXIMUM length of 200 words and a minimum of 100 words. ART DIRECTION is always the exact WORDS in each scene. Output the story in the following format:

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

            Use words like "HD" and "hyperrealistic" in your art direction to ensure a crisp image. Do not repeat descriptions from the scene in the ARE DIRECTION. The ART DIRECTION should only contain direction for coloring and drawing of the image."""
        
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": summary},
             ]
        )
        return response.choices[0].message.content
        
        
        

    def getPropmtsFromNotes(self, notes):
        """This function takes a path as input and returns a list of prompts as output"""
        # create a list of prompts
        prompts = []
        
        return prompts

if __name__ == "__main__":
    summarizer = Summarizer()
    notes = summarizer.readNotesFromPath("data//dummy//input//the_sprawl//")

    pre_summary = summarizer.preSummary(notes)
    summary = summarizer.summarizePreSummaries(pre_summary)
    prompts = summarizer.createPromptFromSummaries(summary)
    
    print(prompts)
    