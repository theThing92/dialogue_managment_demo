"""
Module for Natural Language Understanding.
"""
from enum import Enum
import re

# - preprocessing
#   - remove stopwords, interpunctuation, lower-casing

# - grammar for nlu
class Grammar(Enum):
    response1 = r""
    response2 = r""
    response3 = r""

#   extraction from information from user input (with regular expressions)
#   transfer information to dialogue registry?

class NLU:
    def ___init(self):
        # model: statistical vs. handcrafted
        pass

    def interpret_input(self, user_input):
        # update DR
        # evaluate to system response
        pass
