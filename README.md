This is the implementation of classic PONG game in Python with PyGame library. This game is using Python 3.11 and PyGame 2.6.1. 

Game Rules:
* The game involves hitting a ball using two paddles: the left one (player 1) and the right one (either the AI or player 2).
* The goal is to score 7 points before your opponent. A point is scored when your opponent misses the ball.
* Player 1 controls the paddle using the W (up) and S (down) keys.
* If Player vs. Player mode is selected, Player 2 controls the paddle with the up and down arrow keys. In Player vs. AI mode, the right paddle is controlled by the computer.
* The AI has a random error to ensure it is not invincible.
* When one side scores a point, the ball and paddles return to their starting positions.
* When one player reaches 7 points, a winner is displayed and a new game can begin.

Additional information:
* The game has a simple start screen with game mode selection (keys 1 or 2).
* The score is displayed at the top of the screen.
* Ball bounces off the walls and paddles are signaled by sounds.
* The code uses the Game_Settings.py configuration file to store game constants (sizes, colors, speeds, etc.).
