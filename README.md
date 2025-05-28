# Ludo Game

A classic Ludo board game with graphical interface built using Python and Pygame.

## Features
- Complete Ludo game with 4 players (Red, Green, Blue, Yellow)
- Dice rolling animation
- Token movement with proper game rules
- Win condition detection
- Restart game functionality

## Requirements
- Python 3.6+
- Pygame 2.5.2+

## Installation
1. Clone this repository
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

## Running the Game
Run the game using Python:
```
python ludo_game.py
```

## Creating Windows Executable
To create a Windows executable:
1. Install cx_Freeze:
   ```
   pip install cx_Freeze
   ```
2. Run the build command:
   ```
   python setup.py build
   ```
3. The executable will be created in the build directory

## How to Play
- Click the "Roll Dice" button to roll the dice
- Click on a token to move it according to the dice value
- To move a token out of home, you need to roll a 6
- If you roll a 6, you get an extra turn
- The first player to get all four tokens to the center wins