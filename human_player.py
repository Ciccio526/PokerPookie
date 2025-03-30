class HumanPlayer():
    def __init__(self, name="You"):
        super().__init__()
        self.name = name 
        self.chips = 1000
        self.hand = []
        self.folded = False
        self.selected_action = None
        self.raise_amount = 5

    def set_action(self, action, amount=None):
        self.selected_action = action
        if(amount):
            self.raise_amount = amount

    def act(self, game_state):
        while self.selected_action is None:
            pass
        
        action = self.selected_action
        self.selected_action = None

        if(action == "fold"):
            self.folded = True
            print(f"{self.name} folds")
            return "fold"
        elif(action == "call"):
            self.chips -= self.raise_amount
            print(f"{self.name} calls")
            return "call"
        elif (action == "raise"):
            raise_amount = self.raise_amount
            self.chips -= raise_amount
            print(f"{self.name} raises {raise_amount}")
            return f"raise: {self.raise_amount}"

        return "fold"



    



        




