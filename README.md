Frontlines - Python Tower Defense

**Description**
Frontlines is a 2D tower defense game built entirely in Python using the pygame library. This project serves as a demonstration of Object-Oriented Programming (OOP) principles, game loop mechanics, and dynamic entity management.

**Key Features**

- Interactive UI: Features a main menu with a functional, custom-built volume control slider that directly interacts with the game's audio mixer.

- Dynamic Wave System: Enemies spawn in waves, with their health dynamically scaling up based on the current round number.

- Strategic Tower Placement: Players can spend starting currency to place two distinct types of towers (costing 100 and 200). The placement system includes boundary and collision detection to ensure towers cannot be stacked or placed off-screen.

- Combat & Economy: Towers utilize a cooldown system and trigonometry-based target tracking to fire projectiles at enemies. Defeating enemies rewards the player with money to expand their defenses and increases their overall score.

- Game State Management: Tracks enemy pathing and triggers a dedicated Game Over screen via subprocesses if an enemy successfully breaches the defenses, allowing the player to retry.


**Software Used**

Python 3.8 + Pygame Library (for rendering, event handling, and audio)


**How to Run**

- Intall Python on your device if not already there.

- Install the Pygame library by running: pip install pygame in command prompt

- Clone this repository to your local device.

- Run the main menu file to launch the game: python "main menu.py"
 
