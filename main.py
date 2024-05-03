import random
import os
import time
import json
import sqlite3
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_card_value(rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    @staticmethod
    def get_card_value(rank):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
        return values[rank]

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in ["Hearts", "Diamonds", "Spades", "Clubs"] for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

def deal_initial_cards(player, dealer, deck):
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

def hit(player, deck):
    picked_card = deck.deal_card()
    player.add_card(picked_card)
    console.print(f"\n" + "="*20)
    console.print(f"A {picked_card} was drawn from the deck.")
    console.print("="*20)
    time.sleep(1)

def stand(player):
    pass

def format_cards(cards):
    if isinstance(cards, Card):
        return str(cards)
    else:
        str_cards = ""
        for card in cards:
            str_cards += str(card) + ", " if card != cards[-1] else "and " + str(card)
        return str_cards

def play_game():
    console.print("\n" + "#"*20)
    console.print("Welcome to Blackjack!")
    console.print("#"*20 + "\n")
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    time.sleep(1)

    deal_initial_cards(player_hand, dealer_hand, deck)

    while True:
        console.print("\n" + "="*20)
        console.print("Player's hand:", format_cards(player_hand.cards), "# Current value:", player_hand.value)
        console.print("Dealer's up card:", format_cards(dealer_hand.cards[0]))
        console.print("="*20 + "\n")

        if player_hand.value == 21:
            return "Player wins with a Blackjack!"
        elif player_hand.value > 21:
            return "Player busts! Dealer wins."
        else:
            action = Prompt.ask("Do you want to hit or stand? ").lower()
            if action == 'hit':
                hit(player_hand, deck)
            elif action == 'stand':
                console.print("="*20)
                console.print("Player stands.")
                console.print("="*20)
                console.print("\n" + "="*20)
                console.print("Dealer's hand:", format_cards(dealer_hand.cards), "# Current value:", dealer_hand.value)
                console.print("="*20 + "\n")
                time.sleep(2)
                while dealer_hand.value < 17:
                    hit(dealer_hand, deck)
                    console.print("\n" + "="*20)
                    console.print("Dealer's hand:", format_cards(dealer_hand.cards), "# Current value:", dealer_hand.value)
                    console.print("="*20 + "\n")
                if dealer_hand.value > 21:
                    console.print("="*20)
                    console.print("Dealer busts! Player wins.")
                    console.print("="*20)
                elif dealer_hand.value > player_hand.value:
                    console.print("="*20)
                    console.print("Dealer wins.")
                    console.print("="*20)
                elif dealer_hand.value < player_hand.value:
                    console.print("="*20)
                    console.print("Player wins.")
                    console.print("="*20)
                break
            else:
                console.print("="*20)
                console.print("Invalid action. Please enter 'hit' or 'stand'.")
                console.print("="*20)

    result = Prompt.ask("Do you want to play again? (yes/no) ").lower()
    if result != 'yes':
        save_game_state(player_hand, dealer_hand, deck, "game_over")
    return result

def save_game_state(player_hand, dealer_hand, deck, game_state):
    conn = sqlite3.connect('blackjack.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS game_state (player_hand TEXT, dealer_hand TEXT, deck TEXT, game_state TEXT)')
    c.execute("INSERT INTO game_state VALUES (?, ?, ?, ?)", 
               (json.dumps([str(card) for card in player_hand.cards]), 
                json.dumps([str(card) for card in dealer_hand.cards]), 
                json.dumps([str(card) for card in deck.cards]), 
                json.dumps(game_state)))
    conn.commit()
    conn.close()

def load_game_state():
    conn = sqlite3.connect('blackjack.db')
    c = conn.cursor()
    c.execute('SELECT * FROM game_state')
    row = c.fetchone()
    if row:
        player_hand = Hand()
        dealer_hand = Hand()
        deck = Deck()
        for card in json.loads(row[0]):
            player_hand.add_card(Card(card.split(' of ')[1], card.split(' of ')[0]))
        for card in json.loads(row[1]):
            dealer_hand.add_card(Card(card.split(' of ')[1], card.split(' of ')[0]))
        for card in json.loads(row[2]):
            deck.add_card(Card(card.split(' of ')[1], card.split(' of ')[0]))
        game_state = json.loads(row[3])
        return player_hand, dealer_hand, deck, game_state
    else:
        return None

def delete_database():
    os.remove('blackjack.db')

def create_database():
    conn = sqlite3.connect('blackjack.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS game_state (player_hand TEXT, dealer_hand TEXT, deck TEXT, game_state TEXT)')
    conn.commit()
    conn.close()

create_database()

while True:
    try:
        load_result = load_game_state()
        if load_result:
            player_hand, dealer_hand, deck, game_state = load_result
        else:
            deck = Deck()
            player_hand = Hand()
            dealer_hand = Hand()
            deal_initial_cards(player_hand, dealer_hand, deck)
            game_state = "playing"

        result = play_game()
        console.print("\n" + "="*20)
        console.print(result)
        console.print("="*20 + "\n")
        save_game_state(player_hand, dealer_hand, deck, "game_over")
        play_again = Prompt.ask("Do you want to play again? (yes/no) ").lower()
        if play_again != 'yes':
            break
    except KeyboardInterrupt:
        delete_database()
        break

delete_database()