from human_player import HumanPlayer
from opponent_player import OpponentPlayer
import hand_strength_estimation as HSE


class GameManager:
    def __init__(self, players, table_cards):
        self.players = players
        self.table_cards = table_cards
        self.current_turn = 0
        self.current_round = "preflop"
        self.bFlop = False
        self.bFourth_flip = False
        self.bFifth_flip = False
        self.current_player = players[0]
        self.current_pot = 0
        self.current_bet = 0
        self.winner = ""
        self.raise_player_dict = {player: False for player in self.players}

    #move to PLAYER next turn
    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)
        self.current_player = self.players[self.current_turn]

        

    #move to next Poker Round
    def next_round(self):
        rounds = ["preflop", "flop", "turn", "river", "final"]
        index = rounds.index(self.current_round)

        if(self.raise_player_dict.__contains__(True)):
            pass

        if(index < len(rounds) -1):
            self.current_round = rounds[index+1]
            self.current_turn = 0

        if (self.current_round == rounds[1]):
            self.bFlop = True
        if (self.current_round == rounds[2]):
            self.bFourth_flip = True
        if (self.current_round == rounds[3]):
            self.bFifth_flip = True
        
        if rounds[index] == "final":
            self.winner = self.win()

        self.raise_player_dict = {player: False for player in self.players}

        self.current_bet = 0

    def AI_TakeTurn(self, AI_Player):
        if(self.current_round == "preflop"):
            hand_strength = HSE.give_advice(AI_Player.hand, self.table_cards)
        else:
            hand_strength = HSE.give_advice(AI_Player.hand, self.table_cards)

        return AI_Player.make_decision(hand_strength)

    def win(self):
        player_hand_strength_dict = {}
        for player in self.players:
            if(isinstance(player, HumanPlayer)):
                hand_strength = HSE.hand_strength_sim(HSE.convert_pokerkit_to_treys(player.hand), HSE.convert_pokerkit_to_treys(self.table_cards))
                player_hand_strength_dict[player.name] = hand_strength

        if player_hand_strength_dict:
            best_player = max(player_hand_strength_dict, key=player_hand_strength_dict.get)
                
        return best_player



                



    