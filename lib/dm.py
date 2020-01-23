"""
Module for dialog managment.
"""
from lib.nlu import NLU
from lib.nlg import NLG
from lib.training import Trainer

class DM:

    def __init__(self, type="hard-coded"):

        if type in ("hard-coded", "statistical"):
            self.type = type
        else:
            raise ValueError("'type' must be one of 'hard-coded' or 'statistical'")

        self.stat_model = None
        if self.type == "statistical":
            self.stat_model = Trainer().load().model

        self.current_user_input = None
        self.current_user_int = None

        self._slots = {"pizza_quantity":None, "pizza_type":None, "pizza_size":None}

        # value range system action 1..14
        # value range task-dependent & task-independant information 0..2
        self._dialogue_registry ={'PREV_SYSTEM_ACTION': None,
                                  'TypeOrder': 0,
                                  'NumberPizzas': 0,
                                  'TypesPizzas': 0,
                                  'SizesPizzas': 0,
                                  'TypesDoughs': 0,
                                  'Drinks': 0,
                                  'Acceptance': 0,
                                  'Rejection': 0,
                                  'NotUnderstood': 0,
                                  'SYSTEM_ACTION': 1}

        self._nlu = NLU()
        self._nlg = NLG()


    def evaluate_turn(self):

        if self.type == "hard-coded":

            # initialize dm
            if self._dialogue_registry["PREV_SYSTEM_ACTION"] is None:
                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                # update value dict
                if self.current_user_int == "order" and any(list(slots.values())):
                    # update slots
                    for k,v in slots.items():
                        if v is not None:
                            self._slots[k] = v

                            # update dialogue registry
                            if k == "pizza_quantity":
                                self._dialogue_registry["NumberPizzas"] = 1

                            elif k == "pizza_type":
                                self._dialogue_registry["TypesPizzas"] = 1

                            elif k == "pizza_size":
                                self._dialogue_registry["SizesPizzas"] = 1


                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                return True


            # determine penultima system response, check if it gets accepted or rejected
            elif all(list(self._slots.values())) and\
                    self._dialogue_registry["NumberPizzas"] == 1 and \
                    self._dialogue_registry["TypesPizzas"] == 1 and \
                    self._dialogue_registry["SizesPizzas"] == 1 and \
                    self._dialogue_registry["SYSTEM_ACTION"] != 14:

                self._dialogue_registry["NotUnderstood"] == 0

                if self._dialogue_registry["SYSTEM_ACTION"] == 3:
                    self._dialogue_registry["SYSTEM_ACTION"] = 9
                    self._dialogue_registry["PREV_SYSTEM_ACTION"] = 3

                elif self._dialogue_registry["SYSTEM_ACTION"] == 4:
                    self._dialogue_registry["SYSTEM_ACTION"] = 10
                    self._dialogue_registry["PREV_SYSTEM_ACTION"] = 4

                elif self._dialogue_registry["SYSTEM_ACTION"] == 5:
                    self._dialogue_registry["SYSTEM_ACTION"] = 11
                    self._dialogue_registry["PREV_SYSTEM_ACTION"] = 5

                elif self._dialogue_registry["SYSTEM_ACTION"] == 1:
                    self._dialogue_registry["SYSTEM_ACTION"] = 9
                    self._dialogue_registry["PREV_SYSTEM_ACTION"] = 1

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                # user accepts order
                if self.current_user_int == "acceptance":
                    self._dialogue_registry["Acceptance"] = 1
                    self._dialogue_registry["Rejection"] = 0
                    self._dialogue_registry["SYSTEM_ACTION"] = 14
                    self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)
                    return False

                # user rejects order
                elif self.current_user_int == "rejection":
                    if self._dialogue_registry["SYSTEM_ACTION"] == 9:
                        self._dialogue_registry["Acceptance"] = 0
                        self._dialogue_registry["Rejection"] = 1
                        self._dialogue_registry["SYSTEM_ACTION"] = 3


                    elif self._dialogue_registry["SYSTEM_ACTION"] == 10:
                        self._dialogue_registry["Acceptance"] = 0
                        self._dialogue_registry["Rejection"] = 1
                        self._dialogue_registry["SYSTEM_ACTION"] = 4

                    elif self._dialogue_registry["SYSTEM_ACTION"] == 11:
                        self._dialogue_registry["Acceptance"] = 0
                        self._dialogue_registry["Rejection"] = 1
                        self._dialogue_registry["SYSTEM_ACTION"] = 5

                    else:
                        self._dialogue_registry["Acceptance"] = 0
                        self._dialogue_registry["Rejection"] = 1
                        self._dialogue_registry["SYSTEM_ACTION"] = 3

                    self._dialogue_registry["NumberPizzas"] = 0
                    self._dialogue_registry["TypesPizzas"] = 0
                    self._dialogue_registry["SizesPizzas"] = 0

                    self._slots = {"pizza_quantity": None, "pizza_type": None, "pizza_size": None}

                    self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                    self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                    self.current_user_input = input()

                    slots, user_int = self._nlu.interpret_input(self.current_user_input)

                    self.current_user_int = user_int

                    # update value dict
                    if user_int == "order" and any(list(slots.values())):
                        # update slots
                        for k, v in slots.items():
                            if v is not None:
                                self._slots[k] = v

                                # update dialogue registry
                                if k == "pizza_quantity":
                                    self._dialogue_registry["NumberPizzas"] = 1

                                elif k == "pizza_type":
                                    self._dialogue_registry["TypesPizzas"] = 1

                                elif k == "pizza_size":
                                    self._dialogue_registry["SizesPizzas"] = 1

                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                return True

            # all slots have been filled and accepted
            elif self._dialogue_registry["SYSTEM_ACTION"] == 14 and \
                    self._dialogue_registry["Acceptance"] == 1 and \
                    self._dialogue_registry["Rejection"] == 0 and \
                    self._dialogue_registry["NotUnderstood"] == 0:
                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                return True


            # partially filled
            # +type, -size, -quantity
            elif self._dialogue_registry["TypesPizzas"] == 1 and \
                    self._dialogue_registry["SizesPizzas"] == 0 and \
                    self._dialogue_registry["NumberPizzas"] == 0:

                self._dialogue_registry["SYSTEM_ACTION"] = 5

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                if self.current_user_int == "order":
                    self._dialogue_registry["NumberPizzas"] = 1
                    self._dialogue_registry["SYSTEM_ACTION"] = 9

                    self._slots["pizza_type"] = self.current_user_input

                # self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                return True

            # -type, +size, -quantity
            elif self._dialogue_registry["TypesPizzas"] == 0 and \
                    self._dialogue_registry["SizesPizzas"] == 1 and \
                    self._dialogue_registry["NumberPizzas"] == 0:

                self._dialogue_registry["SYSTEM_ACTION"] = 4

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                if self.current_user_input in ("marinara", "margherita", "barbecue", "sicilian"):
                    self.current_user_int = "order"
                    self._dialogue_registry["TypesPizzas"] = 1
                    self._dialogue_registry["SYSTEM_ACTION"] = 10

                    self._slots["pizza_type"] = self.current_user_input

                # self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                return True

            # -type, -size, +quantity
            elif self._dialogue_registry["TypesPizzas"] == 0 and \
                    self._dialogue_registry["SizesPizzas"] == 0 and \
                    self._dialogue_registry["NumberPizzas"] == 1:

                self._dialogue_registry["SYSTEM_ACTION"] = 4

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                if self.current_user_input in ("marinara", "margherita", "barbecue", "sicilian"):
                    self.current_user_int = "order"
                    self._dialogue_registry["TypesPizzas"] = 1
                    self._dialogue_registry["SYSTEM_ACTION"] = 10

                    self._slots["pizza_type"] = self.current_user_input

                # self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                return True

            # +type, -size, +quantity
            elif self._dialogue_registry["TypesPizzas"] == 1 and \
                    self._dialogue_registry["SizesPizzas"] == 0 and \
                    self._dialogue_registry["NumberPizzas"] == 1:

                self._dialogue_registry["SYSTEM_ACTION"] = 5

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                if self.current_user_input in ("large","extra large","small"):
                    self.current_user_int = "order"
                    self._dialogue_registry["TypesPizzas"] = 1
                    self._dialogue_registry["SYSTEM_ACTION"] = 11

                    self._slots["pizza_size"] = self.current_user_input

                # self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                return True

            # +type, +size, -quantity
            elif self._dialogue_registry["TypesPizzas"] == 1 and \
                    self._dialogue_registry["SizesPizzas"] == 1 and \
                    self._dialogue_registry["NumberPizzas"] == 0:

                self._dialogue_registry["SYSTEM_ACTION"] = 3

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                if self.current_user_int == "order":
                    self._dialogue_registry["NumberPizzas"] = 1
                    self._dialogue_registry["SYSTEM_ACTION"] = 9

                    self._slots["pizza_quantity"] = self.current_user_input

                # self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                return True

            # -type, +size, +quantity
            elif self._dialogue_registry["TypesPizzas"] == 0 and \
                    self._dialogue_registry["SizesPizzas"] == 1 and \
                    self._dialogue_registry["NumberPizzas"] == 1:

                self._dialogue_registry["SYSTEM_ACTION"] = 4

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                if self.current_user_input in ("marinara","margherita","barbecue","sicilian"):
                    self.current_user_int = "order"
                    self._dialogue_registry["TypesPizzas"] = 1
                    self._dialogue_registry["SYSTEM_ACTION"] = 10

                    self._slots["pizza_type"] = self.current_user_input

                #self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

                return True

            # handle unknown
            elif self.current_user_int is None:
                self._dialogue_registry["NotUnderstood"] == 1
                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                return True

            # help caller
            elif self.current_user_int == "help":
                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                self.current_user_input = input()

                slots, user_int = self._nlu.interpret_input(self.current_user_input)

                self.current_user_int = user_int

                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

                return True


        elif self.type == "statistical":

            # need to set non-None value for PREV_SYSTEM_ACTION as no empty values are allowed
            # for predicting with a scikit-learn classifier
            if self._dialogue_registry["PREV_SYSTEM_ACTION"] == None:
                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)
                self._dialogue_registry["PREV_SYSTEM_ACTION"] = 1

            else:
                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]

            prediction_system_reaction = self.stat_model.predict([list(self._dialogue_registry.values())[:-1]])[0]
            self._dialogue_registry["SYSTEM_ACTION"] = prediction_system_reaction

            if self._dialogue_registry["PREV_SYSTEM_ACTION"] != 1:
                self._nlg.generate_response(self._dialogue_registry, self._slots, self.current_user_int)

            if not (self._dialogue_registry["SYSTEM_ACTION"] == 14 and self._dialogue_registry["Acceptance"] in [0, 1]):
                self.current_user_input = input()

            slots, user_int = self._nlu.interpret_input(self.current_user_input)

            self.current_user_int = user_int

            if self.current_user_input in ("marinara", "margherita", "barbecue", "sicilian"):
                self._dialogue_registry["TypesPizzas"] = 1
                self._slots["pizza_type"] = self.current_user_input

            elif self.current_user_input in ("large", "extra large", "small"):
                self._dialogue_registry["SizesPizzas"] = 1
                self._slots["pizza_size"] = self.current_user_input

            self.current_user_int = user_int

            # update value dict
            if self.current_user_int == "order" and any(list(slots.values())):
                # update slots
                for k, v in list(slots.items()):
                    if self._slots[k] is None:
                        self._slots[k] = v

                        if v is not None:
                            # update dialogue registry
                            if k == "pizza_quantity":
                                self._dialogue_registry["NumberPizzas"] = 1

                            elif k == "pizza_type":
                                self._dialogue_registry["TypesPizzas"] = 1

                            elif k == "pizza_size":
                                self._dialogue_registry["SizesPizzas"] = 1

            if all(list(self._slots.values())) and \
                    self._dialogue_registry["NumberPizzas"] == 1 and \
                    self._dialogue_registry["TypesPizzas"] == 1 and \
                    self._dialogue_registry["SizesPizzas"] == 1 and \
                    self._dialogue_registry["SYSTEM_ACTION"] != 14:
                self._dialogue_registry["NotUnderstood"] = 0
                # manual set of system action because of lack of training examples
                self._dialogue_registry["SYSTEM_ACTION"] = 14

                return True

            if all(list(self._slots.values())) and \
                    self._dialogue_registry["NumberPizzas"] == 1 and \
                    self._dialogue_registry["TypesPizzas"] == 1 and \
                    self._dialogue_registry["SizesPizzas"] == 1 and \
                    self._dialogue_registry["SYSTEM_ACTION"] == 14 and \
                    self._dialogue_registry["NotUnderstood"] == 0:

                return False

            elif self.current_user_int == "help":

                return True

            elif user_int == None:
                self._dialogue_registry["NotUnderstood"] == 1

                return True


            elif self.current_user_int == "rejection":
                self._dialogue_registry["Acceptance"] = 0
                self._dialogue_registry["Rejection"] = 1

                return True


            elif self.current_user_int == "acceptance":
                self._dialogue_registry["Acceptance"] = 1
                self._dialogue_registry["Rejection"] = 0

                return False

            else:
                self._dialogue_registry["PREV_SYSTEM_ACTION"] = self._dialogue_registry["SYSTEM_ACTION"]
                return True


if __name__ == "__main__":

    # hard-coded
    print("### Using hard-coded model for inference of system actions ###")
    dm1 = DM("hard-coded")

    flag = True
    while flag:
        flag = dm1.evaluate_turn()

    # statistical
    print("### Using statistical model for inference of system actions ###")
    dm2 = DM("statistical")

    flag = True
    while flag:
        flag = dm2.evaluate_turn()


