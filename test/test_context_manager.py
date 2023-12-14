from django.test import TestCase
import os
from tale import context_manager
from parameterized import parameterized
import json

class ContextManagerTestCase(TestCase):
    #set up context manager
    def setUp(self):
        self.context_manager = context_manager.ContextManager()
        
        
    # parametrize test_get_entities
    @parameterized.expand([
        ("", []),
        ("His name was Eagle.", [("Eagle", "MISC")]),
        ("Eagle entered Die Karibik for the second time in his life", [("Eagle", "MISC"), ("Die Karibik", "MISC")]),
        ("Eagle and Chrom were chased down by TempestTech security personal for hours", [("Eagle", "MISC"), ("Chrom", "MISC"), ("TempestTech", "MISC")]),
        ("Sein Name war Bitwise und er war ein Hacker", []), # NER fails to detect name because of German language but English non-regular name (does not work with pure German pipeline either)
        ("Sein Name war Hans", [("Hans", "PER")]) # obvious name so easier for ner pipeline to detect
    ])
    
    def test_get_entities(self, text, expected_entities):
        entities = self.context_manager.get_entities(text)
        self.assertEqual(entities, expected_entities)
        
        
    # parametrize test_write_entities to test_data/test_context.json
    @parameterized.expand([
        ([("Eagle", "MISC")], os.path.join(os.path.dirname(__file__), "test_data", "test_context.json"), {"Eagle": ""}),
        ([("Eagle", "MISC"), ("Chrom", "MISC")], os.path.join(os.path.dirname(__file__), "test_data", "test_context.json"), {"Eagle": "", "Chrom": ""}),
        ([], os.path.join(os.path.dirname(__file__), "test_data", "test_context.json"), {})
    ])
    
    def test_write_entities(self, entities, filename, expected_context):
        self.context_manager.write_entities(entities, filename)
        expected_context = json.dumps(expected_context)
        with open(filename, "r", encoding="UTF-8") as file:
            context = file.read()
            self.assertEqual(context, expected_context)
            
    # clean up context.json
    def tearDown(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), "test_data", "test_context.json")):
            os.remove(os.path.join(os.path.dirname(__file__), "test_data", "test_context.json"))
    
    