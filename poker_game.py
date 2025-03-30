from logging import warning
from re import X
from pokerkit import Deck, Poker, State
import pygame
import sys
import threading
import queue
import time
from pygame import mouse
import pygame.display
from pygame.rect import Rect
from game_manager import GameManager
from human_player import HumanPlayer
from opponent_player import OpponentPlayer
import pokerkit as pk
import webbrowser


#PLAYER COORDS
coords = [
    (640, 550),
    (150, 300),
    (620, 50),
    (1100, 300)
]

#GENERATE Thinking picture
THINKING_HEIGHT, THINKING_WIDTH = 150, 150
Thinking_Question_image = pygame.transform.scale(pygame.image.load(f"assets/thinkingQ.png"), (THINKING_WIDTH, THINKING_HEIGHT))
Thinking_image = pygame.transform.scale(pygame.image.load(f"assets/thinking.png"), (THINKING_WIDTH, THINKING_HEIGHT))


#generate card pictures
CARD_WIDTH, CARD_HEIGHT = 100, 150
back_of_card = pygame.transform.scale(pygame.image.load(f"assets/CardBack.png"), (CARD_WIDTH, CARD_HEIGHT))
card_images = {}

suits = ["h", "d", "c", "s"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

for suit in suits:
    for rank in ranks:
        filename = f"assets/{rank}_of_{suit}.png"
        card_images[f"{rank}{suit}"] = pygame.transform.scale(pygame.image.load(filename), (CARD_WIDTH, CARD_HEIGHT))


# emotion reading
def read_emotion_data(shared_queue):
    try:
        emotion_data = shared_queue.get()
        return emotion_data
    except:
        return {"emotion" : "Neutral", "Confidence" : 0.0}


#onclick events
def fold_onClick():
    h_player.set_action("fold")

def call_onClick():
    h_player.set_action("call")

def raise_onClick():
    h_player.set_action("raise", 5)
    
def help_onClick():
    webbrowser.open("http://pokerpookie.tech/")


button_list = {
    "Fold": pygame.Rect(195, 550, 100, 50),
    "Call": pygame.Rect(345, 550, 100, 50),
    "Raise": pygame.Rect(495, 550, 100, 50),
    "Help": pygame.Rect(1180, 670, 100, 50)
}


#DEFINE GLOBAL VARIABLES TO USE 
h_player = HumanPlayer("Bob")
AI_One = OpponentPlayer(name="Al")
AI_Two = OpponentPlayer(name="Jim")
AI_Three = OpponentPlayer(name="Lester")
players_list = [h_player, AI_One, AI_Two, AI_Three]

table_cards = []
playing_deck = None
game_manager = None


# GAME SET UP
def set_up_game():
    global playing_deck, table_cards, h_player, game_manager
    playing_deck = pk.Deck.STANDARD
    playing_deck = pk.shuffled(playing_deck) 

    table_cards.extend([playing_deck.pop(), playing_deck.pop(), playing_deck.pop(), playing_deck.pop(),playing_deck.pop()])

    for player in players_list:
        player.hand = [playing_deck.pop(), playing_deck.pop()]

    game_manager = GameManager(players_list, table_cards)

def display_community_cards(screen, flop, fourth_flip, fifth_flip):
    START_X = 300
    if(flop):
        for i in range(3):
            card = table_cards[i]
            card_key = f"{card.rank}{card.suit}"
            card_image = card_images[card_key]
            screen.blit(card_image, (START_X, 250))
            START_X += 150
    else:
        for i in range(3):
            screen.blit(back_of_card, (START_X, 250))
            START_X += 150

    if(not fourth_flip):
        screen.blit(back_of_card, (750, 250))
    if(not fifth_flip):
        screen.blit(back_of_card, (900, 250))

    if(fourth_flip):
        card = table_cards[3]
        card_key = f"{card.rank}{card.suit}"
        card_image = card_images[card_key]
        screen.blit(card_image, (750, 250))

    if(fifth_flip):
        card = table_cards[4]
        card_key = f"{card.rank}{card.suit}"
        card_image = card_images[card_key]
        screen.blit(card_image, (900, 250))

    pygame.display.flip()

def display_player_cards(screen):
    START_X = 750
    for card in h_player.hand:
        card_key = f"{card.rank}{card.suit}"
        card_image = card_images[card_key]
        screen.blit(card_image, (START_X, 550))
        START_X += 150

    pygame.display.flip()

def display_AI_cards(screen, x, y, AI_Player_hand):
    START_X = x
    for card in AI_Player_hand:
        card_key = f"{card.rank}{card.suit}"
        card_image = card_images[card_key]
        screen.blit(card_image, (START_X, y))
        START_X += 115
    pygame.display.flip()

def win_condition(screen):
    font = pygame.font.Font(None, 25)
    if(game_manager.players[1]):
            display_AI_cards(screen, 30, 240, game_manager.players[1].hand)
            AI_one_name = font.render(f"{game_manager.players[1].name}", True, (255,255,255))
            screen.blit(AI_one_name, (30, 400))
    if(game_manager.players[2]):
        display_AI_cards(screen, 500, 30, game_manager.players[2].hand)
        AI_two_name = font.render(f"{game_manager.players[2].name}", True, (255,255,255))
        screen.blit(AI_two_name, (500, 190))

    if(game_manager.players[3]):
        display_AI_cards(screen, 1060, 240, game_manager.players[3].hand)
        AI_three_name = font.render(f"{game_manager.players[3].name}", True, (255,255,255))
        screen.blit(AI_three_name, (1060, 400))

#init logic
pygame.init()
set_up_game()

#Main game loop
def run_poker_game(shared_queue):
    #init GUI
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Poker Trainer")

    global detected_emotion, emotion_confidence, game_manager


    running = True 
    while (running):
        screen.fill((0, 100, 0))

        for text, rect in button_list.items():
            font = pygame.font.Font(None, 25)
            pygame.draw.rect(screen, (0, 0, 100), rect)
            button_label = font.render(text, True, (255, 255, 255))
            screen.blit(button_label, (rect.x + 30, rect.y + 10))
            

        emotion_data = read_emotion_data(shared_queue)
        detected_emotion = emotion_data["emotion"]
        emotion_confidence = emotion_data["confidence"]
        warning_message = ""

        if(detected_emotion == "happy"):
            warning_message = "You are smiling"
        elif(detected_emotion == "surprise"):
            warning_message = "You look surprised"
        elif(detected_emotion == "fear"):
            warning_message = "You look scared"
        elif(detected_emotion == "anger"):
            warning_message = "You look angry"


        font = pygame.font.Font(None, 36)
        emotion_text = font.render(f"{warning_message}", True, (255,255,255))
        
        current_pot_amount_text = font.render(f"Current pot value: ${game_manager.current_pot}", True, (255, 255, 255))
        current_bet_amount_text = font.render(f"Current bet amount: ${game_manager.current_bet}", True, (255, 255, 255))
        current_player_text = font.render(f"Current player: {game_manager.current_player.name}", True, (255,255,255))
        current_coins_text = font.render(f"Current chips: {h_player.chips}", True, (255,255,255))

        display_community_cards(screen, game_manager.bFlop, game_manager.bFourth_flip, game_manager.bFifth_flip)
        display_player_cards(screen)

        screen.blit(emotion_text, (50,50))
        screen.blit(current_bet_amount_text, (195, 460))
        screen.blit(current_pot_amount_text, (195, 480))
        screen.blit(current_player_text, (195, 500))
        screen.blit(current_coins_text, (195,520))

        pygame.display.flip()

        if game_manager.current_player is not h_player:
            if(isinstance(game_manager.current_player, OpponentPlayer) and not game_manager.current_player.folded):

                screen.blit(Thinking_image, coords[game_manager.players.index(game_manager.current_player)])
                pygame.display.flip()

                AI_Decision = game_manager.AI_TakeTurn(game_manager.current_player)
                if(AI_Decision == "raise"):
                    game_manager.current_pot += game_manager.current_bet
                    game_manager.current_bet += game_manager.current_player.raise_amount
                    game_manager.raise_player_dict[game_manager.current_player.name] = True
                elif(AI_Decision == "call"):
                    if(game_manager.current_round == "preflop"):
                        game_manager.current_player.chips -= 1
                        game_manager.current_pot += 1

                    game_manager.current_pot += game_manager.current_bet
                    game_manager.current_player.chips -= game_manager.current_bet
                    game_manager.raise_player_dict[game_manager.current_player.name] = False
                elif(AI_Decision == "fold"):
                    game_manager.current_player.folded = True
                    game_manager.raise_player_dict[game_manager.current_player.name] = False
                game_manager.next_turn()
                pygame.display.flip()
            if game_manager.current_player == h_player:
                game_manager.next_round()

        if(game_manager.winner):
            win_text = font.render(f"Winner; {game_manager.winner}", True, (255,255,255))
            screen.blit(win_text, (195, 600))
            win_condition(screen)

            pygame.display.flip()
            #time.sleep(60)
            


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_manager.current_player is h_player:
                    mouse_pos = event.pos
                    if button_list["Fold"].collidepoint(mouse_pos) :
                        fold_onClick()
                        game_manager.raise_player_dict[game_manager.current_player.name] = False
                        lose_text = font.render(f"Loser", True, (255,255,255))
                        screen.blit(lose_text, (195, 600))
                        pygame.display.flip()

                        display_AI_cards(screen, 30, 240, game_manager.players[1].hand)
                        AI_one_name = font.render(f"{game_manager.players[1].name}", True, (255,255,255))
                        screen.blit(AI_one_name, (30, 400))

                        display_AI_cards(screen, 500, 30, game_manager.players[2].hand)
                        AI_two_name = font.render(f"{game_manager.players[2].name}", True, (255,255,255))
                        screen.blit(AI_two_name, (500, 190))

                        display_AI_cards(screen, 1060, 240, game_manager.players[3].hand)
                        AI_three_name = font.render(f"{game_manager.players[3].name}", True, (255,255,255))
                        screen.blit(AI_three_name, (1060, 400))

                        display_community_cards(screen, True, True, True)

                        pygame.display.flip()
                        time.sleep(60)
                    elif button_list["Call"].collidepoint(mouse_pos):
                        call_onClick()

                        if(game_manager.current_round == "preflop"):
                            game_manager.current_pot += 1
                            game_manager.current_player.chips -= 1

                        game_manager.current_pot += game_manager.current_bet
                        game_manager.raise_player_dict[game_manager.current_player.name] = False
                        game_manager.next_turn()
                    elif button_list["Raise"].collidepoint(mouse_pos):
                        raise_onClick()
                        game_manager.current_bet += h_player.raise_amount
                        game_manager.current_pot += game_manager.current_bet
                        game_manager.raise_player_dict[game_manager.current_player] = True
                        game_manager.next_turn()
                else:
                     print("not your turn")
                     continue
                
                mouse_pos = event.pos
                if button_list["Help"].collidepoint(mouse_pos):
                   help_onClick()
                


        


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pass


