import hand_strength_estimation as HSE
import random
import time

class OpponentPlayer():
    def __init__(self, name="AI"):
        self.name = name 
        self.chips = 1000
        self.hand = []
        self.folded = False
        self.selected_action = None
        self.raise_amount = 5

    def make_decision(self, confidence):
        if confidence > 0.8:  
            self.selected_action = "raise"
        elif confidence > 0.55:  
            print ("Decent hand. Consider a small bet or check.")
            if(random.random() < .05):
                self.selected_action = "raise"
            else:
                self.selected_action = "call"
        elif confidence > 0.35:  
            print ("You have a good draw. Consider calling.")
            if(random.random() < .05):
                self.selected_action = "raise"
            else:
                self.selected_action = "call"
        elif confidence > 0.15:  
            print ("Weak hand, but possible improvement. Call if cheap.")
            if(random.random() < .05):
                self.selected_action = "raise"
            elif(random.random() < .7):
                self.selected_action = "call"
            else:
                self.selected_action = "fold"
        else:
            print ("Your hand is weak. Consider folding.")
            if(random.random() <.9):
                self.selected_action = "fold"
            else:
                self.selected_action = "call"

        decision = self.act()
        time.sleep(random.randint(3, 7))
        return decision


    def act(self):
        
        action = self.selected_action
        self.selected_action = None

        if(action == "fold"):
            self.folded = True
            print(f"{self.name} folds")
            return "fold"
        elif(action == "call"):
            print(f"{self.name} calls")
            return "call"
        elif (action == "raise"):
            raise_amount = self.raise_amount
            self.chips -= raise_amount
            print(f"{self.name} raises {raise_amount}")
            return f"raise"


