"""
Module for Natural Language Generation.
"""
from enum import Enum
from random import choice

class Templates(Enum):
    welcome_prompt = "Welcome to the Pizzeria. Please tell me your order. (Type 'help' to see available pizza types and sizes.)"

    pizza_kind_prompt1 = "What kind of pizza(s) do you want?"
    pizza_kind_prompt2 =  "Please say the name of a pizza, for example sicilian."
    pizza_kind_prompt3 = "Please say the name of a pizza. The four options are marinara, margherita, barbecue and sicilian."

    pizza_quantity_prompt1 = "How many pizza(s) do you want?"
    pizza_quantity_prompt2 = "How many pizza(s) do you want? You can type the quantity as a number (1,2,3...) or spell it out (one, two, three...)."


    pizza_size_prompt1 = "Tell me the size."
    pizza_size_prompt2 = "Please say the size of the pizza(s), for example large."
    pizza_size_prompt3 = "Please say the size of the pizza(s). The options are small, large, and extra large."

    no_match_no_input = "Please say the quantity, size and type of pizza(s) you want. For example, a large sicilian pizza."

    confirmation_order = "You have ordered {} {} {} pizza(s). Is this  correct?"

    help_size_context = "The sizes are small, large, and extra large."
    help_kind_context = "The four types are marinara, margherita, barbecue and sicilian."
    help_quantity_context = "You can type the quantity as a number (1,2,3...) or spell it out (one, two, three...)."

    help_general = f"{help_kind_context}\n{help_size_context}\n{help_quantity_context}"

    closure = "Your pizza will be ready soon. Thank you for using the pizzeria service."

class NLG:
    def __init__(self):
        self._templates = Templates


    def generate_response(self, dialogue_registry, slots, user_int):

        # welcome message from initial dm state
        if dialogue_registry["SYSTEM_ACTION"] == 1 and dialogue_registry["PREV_SYSTEM_ACTION"] != 1:
            print(self._templates.welcome_prompt.value)

        # happy path: all slots have beend filled correctly (closure)
        elif dialogue_registry["SYSTEM_ACTION"] == 14:
            print(self._templates.closure.value)

        # ask for quantity of pizzas
        elif dialogue_registry["SYSTEM_ACTION"] == 3:
            quantity_templates = [self._templates.pizza_quantity_prompt1.value,
                                  self._templates.pizza_quantity_prompt2.value]

            print(choice(quantity_templates))

        # ask for type of pizzas
        elif dialogue_registry["SYSTEM_ACTION"] == 4:
            kind_templates = [self._templates.pizza_kind_prompt1.value,
                              self._templates.pizza_kind_prompt2.value,
                              self._templates.pizza_kind_prompt3.value]

            print(choice(kind_templates))

        # ask for size of pizzas
        elif dialogue_registry["SYSTEM_ACTION"] == 5:
            size_templates = [self._templates.pizza_size_prompt1.value,
                              self._templates.pizza_size_prompt2.value,
                              self._templates.pizza_size_prompt3.value]

            print(choice(size_templates))


        # ask for order cofirmation when all slots are filled
        elif dialogue_registry["SYSTEM_ACTION"] in [9,10,11] and all(list(slots.values())):
            print(self._templates.confirmation_order.value.format(slots["pizza_quantity"],slots["pizza_size"],slots["pizza_type"]))

        # get quantity help
        if dialogue_registry["PREV_SYSTEM_ACTION"] == 3 and user_int == "help":
            print(self._templates.help_quantity_context.value)

        # get type help
        elif dialogue_registry["PREV_SYSTEM_ACTION"] == 4 and user_int == "help":
                print(self._templates.help_kind_context.value)

        # get size help
        elif dialogue_registry["PREV_SYSTEM_ACTION"] == 5 and user_int == "help":
                print(self._templates.help_size_context.value)

        # get general help
        elif dialogue_registry["PREV_SYSTEM_ACTION"] not in [3,4,5] and user_int == "help":
            print(self._templates.help_general.value)


        # no match / no input
        elif dialogue_registry["PREV_SYSTEM_ACTION"] is not None and user_int == None:
            print(self._templates.no_match_no_input.value)


if __name__ == "__main__":
    nlg = NLG()
