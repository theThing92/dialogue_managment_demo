"""
Module for Natural Language Understanding.
"""
from enum import Enum
import re
from nltk.tokenize import RegexpTokenizer
from inflect import engine

class Grammar(Enum):
    order = r"(i)?\s?(want)?\s?(\d{1,2}|\w+)?\s?(large|extra large|small)?\s?(marinara|margherita|barbecue|sicilian)?\s?(pizza|pizzas)?\s?(please)?"
    acceptance = r"(yes|y|ya)"
    rejection = r"(no|n|nope)"
    help = r"help"


class NLU:

    def __init__(self):
        self._tokenizer = RegexpTokenizer(r'[\w-]+')
        self._grammar = tuple(Grammar)
        self._inflect_engine = engine()

    def preprocess(self,user_input):
        preprocessed_user_input = " ".join(self._tokenizer.tokenize(user_input.lower()))
        return preprocessed_user_input


    @staticmethod
    def text2int(textnum, numwords={}):
        """
        source:
        https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers

        :param textnum:
        :param numwords:
        :return:
        """
        if not numwords:
            units = [
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen",
            ]

            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

            scales = ["hundred", "thousand", "million", "billion", "trillion"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):    numwords[word] = (1, idx)
            for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

        current = result = 0
        for word in textnum.split():
            if word not in numwords:
                raise Exception("Illegal word: " + word)

            scale, increment = numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0

        return result + current

    def interpret_input(self, user_input):

        user_input = self.preprocess(user_input)

        slots = {"pizza_quantity":None, "pizza_type":None, "pizza_size":None}
        user_intent = None

        for i,v in enumerate(self._grammar):
            regex = re.compile(v.value)

            match = regex.search(user_input)

            if match:

                # call help functions
                if v.name == "help" and user_input == "help":
                    user_intent = "help"
                    slots = {"pizza_quantity":None, "pizza_type":None, "pizza_size":None}

                # acceptance of user
                if v.name == "acceptance" and user_input in ("yes", "y", "ya"):
                    user_intent =  "acceptance"
                    slots = {"pizza_quantity": None, "pizza_type": None, "pizza_size": None}

                # rejection of user
                if v.name == "rejection" and user_input in ("no", "n", "nope"):
                    user_intent = "rejection"
                    slots = {"pizza_quantity": None, "pizza_type": None, "pizza_size": None}

                # order matches
                if v.name == "order":
                    # check for quantity
                    try:
                        pizza_quantity = match.group(3)

                        # indefinite article
                        if pizza_quantity in ["a","an"]:
                            slots["pizza_quantity"] = "one"
                            user_intent = "order"

                        # number to words
                        try:
                            int(pizza_quantity)
                            pizza_quantity = self._inflect_engine.number_to_words(pizza_quantity)

                        except ValueError:
                            pass

                        # words to number, number to words
                        try:
                            pizza_quantity = NLU.text2int(pizza_quantity)
                            pizza_quantity = self._inflect_engine.number_to_words(pizza_quantity)

                            slots["pizza_quantity"] = pizza_quantity
                            user_intent = "order"

                        except Exception:
                            pass

                    except IndexError:
                        pass

                    # check for size
                    try:
                        pizza_size = match.group(4)

                        if pizza_size in ("large","extra large","small"):
                            slots["pizza_size"] = pizza_size
                            user_intent = "order"

                    except IndexError:
                        pass

                    # check for pizza type
                    try:
                        pizza_type = match.group(5)

                        if pizza_type in ("marinara","margherita","barbecue","sicilian"):
                            slots["pizza_type"] = pizza_type
                            user_intent = "order"

                    except IndexError:
                        pass

        return slots, user_intent


if __name__ == "__main__":
    nlu = NLU()



