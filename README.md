# Space Invaders

A simple implementation of the classic Space Invaders game using Python and Pygame.

## Requirements

- Python 3.x
- Pygame 2.5.2

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:

```bash
python game.py
```

2. Controls:

- Left Arrow: Move left
- Right Arrow: Move right
- Space: Shoot

## Game Rules

- Control the green player ship at the bottom of the screen
- You have 3 health points (shown as green squares in the top-left corner)
- Shoot the red enemy ships before they reach the bottom
- Avoid enemy bullets - getting hit reduces your health
- The game ends if:
  - You lose all 3 health points
  - Any enemy ship reaches the bottom of the screen
  - You destroy all enemy ships (Victory!)

## Features

- Simple and clean graphics
- Smooth controls
- Player health system
- Enemy shooting mechanics
- Collision detection
- Enemy movement patterns
- Bullet mechanics
- Visual health indicator
