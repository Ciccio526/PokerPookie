from tracemalloc import start
from main_menu import startMenu
import threading
import queue
import cv2
import sys
from facial_analysis import analyze_face, display_camera_feed
import main_menu


if __name__ == "__main__":
    # Create shared queue for inter-thread communication
    shared_queue = queue.Queue()

    #Creating an event to trigger starting the game
    start_game_event = threading.Event()

    #open start menu and pass event, waitng for it to be triggered
     # Start the main menu on the main thread
    menu_thread = threading.Thread(target=startMenu, args=(start_game_event,))
    menu_thread.start()

    #Waits for event to be triggered
    start_game_event.wait()

    # Detect emotion and pass them to a shared queue
    facial_input = cv2.VideoCapture(0)

    # Start the facial analysis thread
    from poker_game import run_poker_game

    facial_analysis_thread = threading.Thread(target=analyze_face, args=(shared_queue, facial_input))
    facial_analysis_thread.daemon = True
    facial_analysis_thread.start()

    # Start the poker game thread
    game_thread = threading.Thread(target=run_poker_game, args=(shared_queue,))
    game_thread.daemon = True
    game_thread.start()

    # Display camera feed
    display_camera_feed(facial_input)

    # Wait for threads to finish
    facial_analysis_thread.join()
    game_thread.join()
