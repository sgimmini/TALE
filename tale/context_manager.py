import spacy
from .pre_processor import PreProcessor
import json
import os

# class ContextManager to do NER tagging to find names of people, places, and organizations
class ContextManager:
    def __init__(self, model='xx_ent_wiki_sm'):
        self.nlp = spacy.load(model)
        self.pre_processor = PreProcessor()

    def get_entities(self, text):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            if(ent.label_ == "PER"):
                entities.append((ent.text, ent.label_))
                print(ent.text, ent.label_)
        return entities
    
    # write entities to context.json
    def write_entities(self, entities, filename=os.path.join(os.path.dirname(__file__), "..", "media", "uploads","context.json")):
        # transform entities to dict
        entity_dict = {}
        for i in range(len(entities)):
            entity_dict[entities[i][0]] = ""
        
        # json string from dict
        json_string = json.dumps(entity_dict)
        
        # write json string to file
        self.pre_processor.write_file(json_string, filepath=filename)
