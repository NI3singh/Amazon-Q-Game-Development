# Amazon-Q-Game-Development

# Neural Challenger

A brain-training game that challenges both your cognitive abilities and reflexes simultaneously.

![Neural Juggler Game](https://github.com/yourusername/neural-juggler/raw/main/screenshots/gameplay.png)

## Game Description

Neural Challenger puts you in the role of a circus performer who must juggle both mental puzzles and physical dexterity at the same time. The screen is split
into two panels:

1. Puzzle Panel (Left) - Presents a mini cognition challenge every 10 seconds:
   • Simon Says memory sequences
   • Quick math problems
   • Stroop-style word/color mismatches

2. Reflex Panel (Right) - Continuously drops shapes from the top:
   • Control a cursor at the bottom to catch only the target shape
   • Avoid catching incorrect shapes

You need to keep both tasks going simultaneously. If you miss a target shape, fail to avoid a wrong shape, or fail a puzzle, you lose a "juggle ball." Lose
all three balls and the show ends!

## Features

• **Dual-task gameplay** that challenges different cognitive systems
• **Three distinct puzzle types** that test different mental abilities
• **Progressive difficulty** as your score increases
• **Score tracking** and life system
• **Colorful visuals** and intuitive controls

## Installation

1. Clone this repository:
git clone https://github.com/yourusername/neural-juggler.git


2. Install the required dependencies:
pip install pygame


3. Run the game:
python neural_challenger.py


## How to Play

• **Left Panel**: Solve the cognitive puzzles before time runs out
  • Simon Says: Click the colored buttons in the correct sequence
  • Math Problems: Type the answer and press Enter
  • Stroop Test: Click the color of the text (not the word itself)

• **Right Panel**: Use the left and right arrow keys to move the catcher
  • Catch only the target shape type (shown at the top)
  • Avoid catching other shapes

## Code Structure

The game is built using Python and Pygame, with the following structure:

• neural_challenger.py - Main game file containing all game logic
• Classes:
  • Shape - Manages the falling shapes
  • Cursor - Controls the player's catcher
  • SimonPuzzle, MathPuzzle, StroopPuzzle - Different puzzle types
