# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ValidateOrderForm(FormValidationAction):
    def name(self):
        return "validate_order_form"

    """
        Storing a list of supported dishes offered in the restaurant.
    """
    @staticmethod
    def menu_db(menu_type) -> List[Text]:
        if menu_type == 'main':
            price_dict = {'cheeseburger': 25, 'filet o fish': 35, 'big mac': 50, \
                          'quarter pounder': 45, 'mcchicken': 25, 'mcdouble': 30, \
                              'angus beef burger': 75}
                
            return ["cheeseburger", "filet o fish", "big mac", "quarter pounder", \
                    "mcchicken", "mcdouble", "angus beef burger"]
        elif menu_type == 'side':
            price_dict = {'coke': 8, 'sprite': 8, 'coffee': 15, 'milk tea': 25}
            
            return ['coke', 'sprite', 'coffee', 'milk tea']
        
    def fetch_slots(tracker):
        ordered_items = []
        main_ordered = tracker.get_slot(user_main)
        if main_ordered is not None:
            ordered_items.append(main_ordered)
            
        return ordered_items
    
    def validate_user_main(self, slot_value, dispatcher, tracker, domain):
        if slot_value.lower() in self.menu_db("main"):
            return {"user_main": slot_value}
    
        else:
            return {"user_main": None}
        
    def validate_user_side(self, slot_value, dispatcher, tracker, domain):
        if slot_value.lower() in self.menu_db("side"):
            return {"user_side": slot_value}
    
        else:
            return {"user_side": None}
    
    async def run(self, dispatcher, tracker, domain):
        continue
            