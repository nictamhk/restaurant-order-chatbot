# This files contains custom actions which can be used to run
# custom Python code.

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
#from rasa_sdk.forms import FormAction

### GLOBAL VARIABLE - Menu of the restaurant
MENU = {
        'main': {'cheeseburger': 25, 'filet o fish': 35, 'big mac': 50, \
              'quarter pounder': 45, 'mcchicken': 25, 'mcdouble': 30, \
            'angus beef burger': 75}, \
        'side': {'fries': 13, 'hash brown': 10, 'cone': 8},
        'drink': {'coke': 8, 'sprite': 8, 'coffee': 15, 'milk tea': 25}
        }

### TEST CLASS
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

### VALIDATES IF THE ITEM IS IN THE MENU
class ValidateOrderForm (FormValidationAction):
    def name(self):
        return "validate_order_form"
    
    def to_lower(self, item):
        if item is not None:
            return item.lower()
        
        else:
            return None
    
    async def run(self, dispatcher, tracker, domain):
        # Grab items ordered
        user_main = self.to_lower(tracker.get_slot("user_main"))
        user_side = self.to_lower(tracker.get_slot("user_side"))
        user_drink = self.to_lower(tracker.get_slot("user_drink"))
        user_drink_size = self.to_lower(tracker.get_slot("user_drink_size"))
        
        # Status of the components ordered
        main_validated = tracker.get_slot("main_validated")
        side_validated = tracker.get_slot("side_validated")
        drink_validated = tracker.get_slot("drink_validated")
        
        # Check if item is offered
        if (user_main is not None and user_main not in MENU['main']):
            dispatcher.utter_message(response = "utter_item_not_offered")
            #return {"user_main": None}
            return [SlotSet("user_main", None)]
        
        elif (user_side is not None and user_side not in MENU['side']):
            dispatcher.utter_message(response = "utter_item_not_offered")
            return [SlotSet("user_side", None)]
            #return {"user_side": None}
        
        elif (user_drink is not None and user_drink not in MENU['drink']):
            dispatcher.utter_message(response = "utter_item_not_offered")
            return [SlotSet("user_drink", None)]
            #return {"user_drink": None}
        
        if (user_main is not None and user_main in MENU['main'] and not main_validated):
            str_confirm = "Alright, so I've got " + user_main + " for your main course."
            dispatcher.utter_message(str_confirm)
            return [SlotSet("user_main", user_main), SlotSet("main_validated", True)]
        
        if (user_side is not None and user_side in MENU['side'] and not side_validated):
            str_confirm = "Got it, " + user_side + " for your side."
            dispatcher.utter_message(str_confirm)
            return [SlotSet("user_side", user_side), SlotSet("side_validated", True)]
            #return {"user_side": user_side} #Validated
        
        if (user_drink is not None and user_drink in MENU['drink'] and not drink_validated):
            str_confirm = "Okay, " + user_drink + " to drink."
            dispatcher.utter_message(str_confirm)
            return [SlotSet("user_drink", user_drink), SlotSet("drink_validated", True)]
            #return {"user_drink": user_drink} #Validated
                
        # Check if drink size has been defined as well
        if (user_drink is not None and user_drink in MENU['drink'] and \
            user_drink_size is None):
            dispatcher.utter_message("What size do you want your " + user_drink + "?")
            return []
        

class CalculateSubTotal (Action):
    def name(self):
        return "action_calculate_total"

    """
        Storing a list of supported dishes offered in the restaurant.
    """
    @staticmethod
    def menu_db(menu_type):
        price_dict = {}
        
        if menu_type == 'main':
            price_dict = {'cheeseburger': 25, 'filet o fish': 35, 'big mac': 50, \
                          'quarter pounder': 45, 'mcchicken': 25, 'mcdouble': 30, \
                        'angus beef burger': 75}
                
            #return ["cheeseburger", "filet o fish", "big mac", "quarter pounder", \
            #        "mcchicken", "mcdouble", "angus beef burger"]
            
        elif menu_type == 'side':
            price_dict = {'fries': 13, 'hash brown': 10, 'cone': 8}
            
        elif menu_type == 'drink':
            price_dict = {'coke': 8, 'sprite': 8, 'coffee': 15, 'milk tea': 25}
            
            #return ['coke', 'sprite', 'coffee', 'milk tea']
            
        return price_dict
        
    def fetch_slots(tracker):
        
        ordered_items = []
        main_ordered = tracker.get_slot("user_main")
        if main_ordered is not None:
            ordered_items.append(main_ordered)
            
        return ordered_items
    
    def get_price(self, entry):
        price = 0
        
        try:
            slot_value = entry[0].lower()
            domain = entry[1]
            price = MENU[domain][slot_value.lower()]
            
        except:
            price = 0
            
        return price
    
    def validate_user_main(self, slot_value, dispatcher, tracker, domain):
        if slot_value.lower() in self.menu_db("main"):
            return {"user_main": slot_value}
    
        else:
            dispatcher.utter_message(response = "utter_item_not_offered")
            return {"user_main": None}
        
    def validate_user_side(self, slot_value, dispatcher, tracker, domain):
        if slot_value.lower() in self.menu_db("side"):
            return {"user_side": slot_value}
    
        else:
            return {"user_side": None}
    
    async def run(self, dispatcher, tracker, domain):
        price = 0
        
        # Grab the ordered items
        main_ordered = (tracker.get_slot("user_main"), "main")
        side_ordered = (tracker.get_slot("user_side"), "side")
        drink_ordered = (tracker.get_slot("user_drink"), "drink")
        
        ordered = [main_ordered, side_ordered, drink_ordered]
        
        # Option when customer wants to confirm order
        confirm_order = tracker.get_slot("confirm_order")
        
        # Track if the user has finished ordering
        end_order = tracker.get_slot("end_order")
        
        # Order status
        curr_subtotal = tracker.get_slot('subtotal')

        for i in ordered:
            price += self.get_price(i)
            return [SlotSet("subtotal", str(price))]
            
        # else:
        #     dispatcher.utter_message(response = "utter_item_not_offered")
        #     price = 0
            
        if confirm_order:
            dispatcher.utter_message("So this is what you've ordered:", \
                                     str(main_ordered or ''), ", ", \
                                     str(side_ordered or ''), ", ", \
                                     str(drink_ordered or ''),
                                     ". Does that sound right?")
        
        if end_order:
            dispatcher.utter_message(response = "utter_total", subtotal = str(curr_subtotal))
            
class confirmOrder (Action):
    def name (self):
        return "confirm_order"
    
    async def run (self, dispatcher, tracker, domain):
        main_ordered = tracker.get_slot("user_main")
        side_ordered = tracker.get_slot("user_side")
        drink_ordered = tracker.get_slot("user_drink")
        
        dispatcher.utter_message("So this is what you've ordered:", \
                                     str(main_ordered or ''), ", ", \
                                     str(side_ordered or ''), ", ", \
                                     str(drink_ordered or ''),
                                     ". Does that sound right?")