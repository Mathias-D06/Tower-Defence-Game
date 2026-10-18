# Frontlines: a Python Tower Defence Game

A 2D tower defence game written in Python with **Pygame**. Enemies march along a winding path in
waves that get bigger and tougher each round. You spend money to place towers that track and shoot
them before they reach the other side of the map.

I built it to practise **object-oriented programming** and real-time game logic: a 60 FPS game loop,
moving entities, collision detection and an in-game economy. It was developed over three prototypes.

🎥 **Demo:** [Prototype 1 validation video](Prototype%201/Prototype%201%20Assets/Prototype%201%20Validation%20%281%29.mp4)

---

## How to play

1. Launch the game. On the main menu, click **Start**. Use **Settings** to set the music volume.
2. Click a tower in the shop at the bottom of the screen, then click on the map to place it.
   Press **Esc** to cancel.
3. Towers fire at enemies in range on their own. Each kill earns money and score, so you can build more.
4. If an enemy gets off the right-hand edge of the map, it's **Game Over**. Click **Play Again** to retry.

| Tower | Cost | Damage per shot |
|---|---|---|
| Tower 1 | 100 | 40 |
| Tower 2 | 200 | 65 |

You start with **200** money. Each kill gives **+20 money** and **+100 score**.

## Features

- **Wave system.** A new wave spawns when the last one is cleared. Waves start at 4 enemies, gain one
  more every 4 rounds (up to 15), and enemy health grows each round.
- **Path following.** Enemies follow a set route across the map, with turns at fixed waypoints.
- **Targeting and projectiles.** Each tower finds an enemy within its 150 px range. Towers spread
  their fire so two towers don't waste shots on the same enemy. Projectiles home in on their target
  using `atan2`, and the sprite rotates to face the direction it's flying.
- **Fire-rate cooldowns.** Each tower can fire once every 450 ms, tracked per tower with a dictionary
  of timestamps.
- **Placement rules.** A tower can't be placed off-screen, on top of another tower, or on an enemy.
  A preview follows the mouse until you click.
- **Economy and HUD.** Money, score and the current round are shown on screen and update live.
- **Menus and audio.** A main menu with background music, a settings screen with a custom-built
  volume slider wired to Pygame's audio mixer, and a Game Over screen with Play Again.

## How the code is organised

| Class | File | Responsibility |
|---|---|---|
| `Tower` | `Prototype 1/tower.py` | Tower stats, range checks, choosing targets, firing and cooldowns, money and score |
| `TowerSelection(Tower)` | `Prototype 1/tower.py` | Inherits from `Tower`; handles shop selection, the placement preview and validating where a tower can go |
| `Projectile` | `Prototype 1/tower.py` | Homing movement, sprite rotation and hit detection |
| `EnemyGroup` | `Prototype 1/tower.py` | Spawning waves, scaling health and moving enemies along the path |
| `MainLoop` | `Prototype 1/tower.py` | The 60 FPS game loop: input, update, draw, HUD and game-over checks |
| `MenuLoop`, `SettingsScreen(MenuLoop)` | `Prototype 2/main menu.py` | Main menu and settings screen |
| `VolumeSlider` | `Prototype 2/main menu.py` | A draggable slider that maps its position to a 0–100 volume |
| `Main` | `Prototype 3/game over.py` | Game Over screen and Play Again |

OOP ideas used:

- **Encapsulation:** private (`__`) and protected (`_`) attributes.
- **Inheritance:** `TowerSelection` from `Tower`, and `SettingsScreen` from `MenuLoop`.
- **Composition:** `MainLoop` owns the tower system and the enemy group.

## Development: three prototypes

1. **Prototype 1, the core game:** map, enemy waves, path following, towers, projectiles, economy
   and HUD.
2. **Prototype 2, the main menu:** Start and Settings buttons, menu music and the volume slider.
3. **Prototype 3, Game Over:** an end screen that relaunches the game.

The menu, game and Game Over screen are separate scripts that launch each other with `subprocess`.

## Running it

Requirements: **Python 3.8+** and **Pygame**, on **Windows**. The asset paths use Windows-style
separators.

```bash
git clone https://github.com/Mathias-D06/Tower-Defence-Game.git
cd Tower-Defence-Game
pip install pygame
python "Prototype 2/main menu.py"
```

Run the command from the repository's root folder, because the game loads its images and sounds
using paths relative to it. Make sure `python` on your PATH is the interpreter that has Pygame
installed, because the menu launches the other screens with that command.

## What I'd improve next

- Move to a single game loop with a state machine (menu → playing → game over) instead of launching
  separate scripts.
- Build asset paths with `os.path` / `pathlib` so the game runs on macOS and Linux too.
- Upgradeable towers, more enemy types and a pause button.
- Save high scores between sessions.

## Credits

Tower, enemy and projectile sprites come from a free tower defence asset pack. Code by
[Mathias Dawit](https://github.com/Mathias-D06).
