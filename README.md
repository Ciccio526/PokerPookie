This project was lead by me, and developed along side a small team for the 2025 ProfHacks Rowan hackathon. 

What it does:
PokerPookie teaches you how to play poker, and keeps you in check so that you are always as serious as possible. It does this through intelligent AI, as well as computer vision, which watches you as you play to warn you if you lose your poker face. PokerPookie also has a handy webiste which you can visit within the main program that tells you about PokerPookie and what it does, as well as useful information about poker itself and info about us, the creators! (pokerpookie.tech)

How we built it:
This program was built in python using PyQt, pygame, DeepFace, and other libraries that allow PookerPookie to be as powerful as it is. pygame is used to run the game loop, most of the game logic, as well as manage/display the GUI. DeepFace is an AI vision model that analyzes a face and detects the most prominent emotion in said face. We utilized this by seeing if a person was happy (smiling), surprised or angry (widened eyes/furled eyebrows), as well as to see if someone was just neutral since that is the optimal poker face. Various libraries were also used to assist in hand strength analysis. The program utilizes pythons multithreading capabilities to ensure that all parts of the program can run simultaneously without issues.

For more information, feel free to visit https://devpost.com/software/poker-pookie
