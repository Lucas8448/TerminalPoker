# Blackjack Game

This Blackjack game is a command-line application developed in Python. The game simulates a classic blackjack card game where you play against the dealer. It features a deck of cards, player and dealer hands, and simple game dynamics, including hitting, standing, and automatic dealer play. The game state is preserved using a SQLite database.

## Features

- Card shuffling and dealing
- Dynamic player interactions (hit or stand)
- Automatic dealer decisions
- Game state saved in a SQLite database
- Simple round-based gameplay loop

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-github/blackjack-game.git
   cd blackjack-game
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

To start the game, run the following command in the terminal:

```bash
python main.py
```

Follow the on-screen prompts to play the game. You can choose to hit or stand during your turn, and the game will continue until you decide to stop.

## Code Overview

- **Database Management:** Uses SQLite to manage game state, including current hands and deck status.
- **Classes:**
  - `Card`: Represents a single card with suit and rank.
  - `Deck`: Handles card shuffling and dealing.
  - `Hand`: Manages the cards for the player and dealer.
  - `BlackjackGame`: Controls game logic, interactions, and maintains the game state.
- **External Libraries:** Utilizes `rich` for enhanced console output and `sqlite3` for database operations.

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests. We appreciate your contributions to enhancing this game!

---

You can save this README as `README.md` in the root directory of your project. Make sure to adjust the repository URL and any specific details about your project setup or additional features you might have added.
