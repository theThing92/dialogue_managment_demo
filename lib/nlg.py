"""
Module for Natural Language Generation.
"""
from enum import Enum

# - system output based on info in dialogue registry and current dialogue state
# - template based nlg

class Templates(Enum):
    template1 = r"a"
    template2 = r"b"
    template3 = r"c"

class NLG:
    def __init__(self):
        # dialogue_manager: exspecially DR
        # templates

        pass

    def generate_response(self):
        pass