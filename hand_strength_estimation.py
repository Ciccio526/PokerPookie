import pokerkit as pk
import treys
from treys import Card, Deck, Evaluator
import random


MIN_STRENGTH = 10_000_000
MAX_STRENGTH = 800_000_000

# Returns a floating point between 0 and 1 based on how strong your hand is
def hand_strength_sim(g_hand, t_cards):
    """
    Evaluates the current strength of a poker hand.

    Args:
        hand (list): The player's hand (2 cards).
        board (list): The community cards.

    Returns:
        float: Strength of the hand (0 = weakest, 1 = strongest).
    """
    evaluator = Evaluator()

    hand_rank = evaluator.evaluate(g_hand, t_cards) # Get hand rank
    max_rank = 7462  # Royal Flush is the highest rank
    return hand_rank / max_rank  # Normalize (0-1)

#find possible future strength, 0-1
def monte_carlo_sim(g_hand, t_cards, sim_num=10000):
    
    # First we create a deck and remove all known cards
    evaluator = Evaluator()

    remaining_deck = [card for card in treys.Deck.GetFullDeck() if card not in g_hand + t_cards]
    wins = 0

    for _ in range(sim_num):
        random.shuffle(remaining_deck)

        simulated_board = t_cards[:]
        while len(simulated_board) < 5:
            simulated_board.append(remaining_deck.pop())

        player_best = evaluator.evaluate(g_hand, simulated_board)

        # Consider a "strong" hand as a straight or better (rank 4+)
        if player_best <= 1000:  # Lower values indicate stronger hands
            wins += 1

    return wins / sim_num  # Probability to improve


def give_advice(given_hand, table_cards):
    strength = hand_strength_sim(convert_pokerkit_to_treys(given_hand), convert_pokerkit_to_treys(table_cards))
    improvement_chance = monte_carlo_sim(convert_pokerkit_to_treys(given_hand), convert_pokerkit_to_treys(table_cards))

    # Define AI strategy rules
    if strength > 0.8:  
        print( "Strong hand! Bet or Raise.")
    elif strength > 0.5:  
        print ("Decent hand. Consider a small bet or check.")
    elif improvement_chance > 0.4:  
        print ("You have a good draw. Consider calling.")
    elif improvement_chance > 0.2:  
        print ("Weak hand, but possible improvement. Call if cheap.")
    else:
        print ("Your hand is weak. Consider folding.")

    return strength

def convert_pokerkit_to_treys(pokerkit_cards):
    """
    Convert a list of pokerkit card strings to treys card objects.
    
    Args:
        pokerkit_cards (list): List of pokerkit card strings (e.g., ['As', '3h']).
    
    Returns:
        list: List of treys card objects.
    """
    # Define suit mapping for treys (Card.new() expects 's', 'h', 'd', 'c')
    suit_map = {'s': 's', 'h': 'h', 'd': 'd', 'c': 'c'}
    
    treys_cards = []
    
    for card in pokerkit_cards:
        # Extract rank and suit

        if isinstance(card, pk.utilities.Card):
            card_string = str(card)

        # Find the position of the opening and closing parentheses
        start = card_string.find('(') + 1
        end = card_string.find(')')
        
        # Extract the substring inside the parentheses
        inside_parentheses = card_string[start:end]
        
        # Get the left and right letters
        rank = inside_parentheses[0]
        suit = inside_parentheses[1]

        # Convert to treys format (Card.new expects string like 'As', '3h', etc.)
        treys_card_str = rank + suit
        treys_card = Card.new(treys_card_str)  # Convert to treys card object
        
        treys_cards.append(treys_card)
    
    return treys_cards


    

