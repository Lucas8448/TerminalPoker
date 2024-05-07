import sqlite3
import json
import random
import time
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Card.get_card_value(rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    @staticmethod
    def get_card_value(rank):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
        return values[rank]

    def to_json(self):
        return {"suit": self.suit, "rank": self.rank}

class Deck:
    def __init__(self):
        self.cards = []
        self.load_deck()
        self.shuffle()

    def load_deck(self):
        with open("deck.json", "r") as f:
            deck_data = json.load(f)
        self.cards = [Card(card["suit"], card["rank"]) for card in deck_data]

    def shuffle(self):
        random.shuffle(self.cards)
        console.print("\nShuffling the deck...\n")
        time.sleep(1.5)  # Pause for effect

    def deal_card(self):
        card = self.cards.pop(0) if self.cards else None
        return card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card, is_dealer=False):
        if card:
            self.cards.append(card)
            self.value += card.value
            display_card = f"hidden card" if is_dealer and len(self.cards) == 1 else card
            actor = "Dealer" if is_dealer else "Player"
            console.print(f"{actor} dealt: {display_card}")
            time.sleep(1)
            if card.rank == 'Ace':
                self.aces += 1
            self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            console.print("Adjusting for Ace...")
            self.value -= 10
            self.aces -= 1
            time.sleep(1)

    def clear(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def to_json(self):
        return [card.to_json() for card in self.cards]

    def from_json(self, cards):
        self.clear()
        for card in cards:
            self.add_card(Card(card["suit"], card["rank"]))

class BlackjackGame:
    def __init__(self, db_path="game.db"):
        self.db_path = db_path
        self.initialize_db()
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.load_game_state()

    def initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS game_states (
            id INTEGER PRIMARY KEY,
            player_hand TEXT,
            dealer_hand TEXT,
            deck TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY,
            result TEXT
        )''')
        conn.commit()
        conn.close()

    def save_game_state(self):
        state = {
            "player_hand": self.player_hand.to_json(),
            "dealer_hand": self.dealer_hand.to_json(),
            "deck": [card.to_json() for card in self.deck.cards]
        }
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM game_states")
        cur.execute("INSERT INTO game_states (player_hand, dealer_hand, deck) VALUES (?, ?, ?)", 
                    (json.dumps(state["player_hand"]), json.dumps(state["dealer_hand"]), json.dumps(state["deck"])))
        conn.commit()
        conn.close()

    def load_game_state(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT player_hand, dealer_hand, deck FROM game_states LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if row:
            self.player_hand.from_json(json.loads(row[0]))
            self.dealer_hand.from_json(json.loads(row[1]))
            self.deck.cards = [Card(card["suit"], card["rank"]) for card in json.loads(row[2])]
        else:
            self.deck.load_deck()
            self.deck.shuffle()

    def log_game_result(self, result):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO game_results (result) VALUES (?)", (result,))
        conn.commit()
        conn.close()

    def play_round(self):
        self.deck.load_deck()
        self.deck.shuffle()
        self.deal_initial_cards()

        while True:
            console.print(f"\n{'='*20}\nPlayer's hand: {self.format_cards(self.player_hand.cards)} # Current value: {self.player_hand.value}")
            console.print(f"Dealer's up card: {self.dealer_hand.cards[1] if len(self.dealer_hand.cards) > 1 else 'hidden card'}\n{'='*20}\n")
            time.sleep(2)
            if self.player_hand.value == 21:
                console.print("Blackjack! Congratulations!")
                time.sleep(1)
                return "Player wins with a Blackjack!"
            elif self.player_hand.value > 21:
                console.print("Bust! Sorry, you went over 21.")
                time.sleep(1)
                return "Player busts! Dealer wins."
            action = Prompt.ask("Do you want to hit or stand?").lower()
            if action == 'hit':
                self.player_hand.add_card(self.deck.deal_card())
            elif action == 'stand':
                console.print(f"\n{'='*20}\nPlayer stands.\n{'='*20}")
                time.sleep(1)
                break
        
        return self.evaluate_winner()

    def deal_initial_cards(self):
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card(), is_dealer=True)
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card(), is_dealer=True)

    def evaluate_winner(self):
        console.print("\nDealer's turn to draw cards...\n")
        console.print(f"Dealer reveals the hidden card: {self.dealer_hand.cards[0]}")
        time.sleep(2)
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal_card(), is_dealer=True)
            time.sleep(1)
        console.print(f"\n{'='*20}\nDealer's hand: {self.format_cards(self.dealer_hand.cards)} # Current value: {self.dealer_hand.value}\n{'='*20}\n")
        if self.dealer_hand.value > 21:
            console.print("Dealer busts!")
            time.sleep(1)
            return "Dealer busts! Player wins."
        elif self.dealer_hand.value > self.player_hand.value:
            return "Dealer wins."
        elif self.dealer_hand.value < self.player_hand.value:
            return "Player wins."
        return "It's a tie!"

    @staticmethod
    def format_cards(cards):
        return ', '.join(str(card) for card in cards[:-1]) + ' and ' + str(cards[-1]) if len(cards) > 1 else str(cards[0])

def main():
    game = BlackjackGame()
    while True:
        result = game.play_round()
        game.log_game_result(result)
        console.print(f"\n{'='*20}\n{result}\n{'='*20}\n")
        game.player_hand.clear()
        game.dealer_hand.clear()
        if Prompt.ask("Do you want to play another game? (yes/no)").lower() != 'yes':
            break
        else:
            console.print("\nStarting a new game...\n")
            time.sleep(1)
            main()

if __name__ == "__main__":
    main()