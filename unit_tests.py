import json
from unittest.mock import patch
import pytest
from main import Card, Deck, Hand, BlackjackGame

@pytest.fixture
def mock_deck_data():
    return [
        {"suit": "Hearts", "rank": "Ace"},
        {"suit": "Diamonds", "rank": "King"},
        {"suit": "Clubs", "rank": "2"},
        {"suit": "Spades", "rank": "10"}
    ]

@pytest.fixture
def card():
    return Card('Hearts', 'Ace')

@pytest.fixture
def deck(mock_deck_data):
    with patch('json.load', return_value=mock_deck_data):
        return Deck()

def test_deck_shuffle(deck):
    original_order = deck.cards[:]
    deck.shuffle()
    assert deck.cards != original_order

def test_deck_deal_card(deck):
    original_count = len(deck.cards)
    card = deck.deal_card()
    assert card is not None
    assert len(deck.cards) == original_count - 1

@pytest.fixture(scope="session")
def setup_database():
    game = BlackjackGame(db_path=":memory:")
    yield game
    game.close_connection()

@pytest.fixture
def game(setup_database):
    setup_database.reset_game()
    return setup_database


def test_card_initialization(card):
    assert card.suit == 'Hearts'
    assert card.rank == 'Ace'
    assert card.value == 11

def test_card_string_representation(card):
    assert str(card) == 'Ace of Hearts'

def test_card_to_json(card):
    assert card.to_json() == {"suit": "Hearts", "rank": "Ace"}

def test_deck_shuffle(deck):
    original_order = deck.cards[:]
    deck.shuffle()
    assert deck.cards != original_order

def test_deck_deal_card(deck):
    original_count = len(deck.cards)
    card = deck.deal_card()
    assert card is not None
    assert len(deck.cards) == original_count - 1

def test_hand_initialization():
    hand = Hand()
    assert hand.cards == []
    assert hand.value == 0
    assert hand.aces == 0

def test_hand_add_card():
    hand = Hand()
    card = Card('Spades', '3')
    hand.add_card(card)
    assert len(hand.cards) == 1
    assert hand.value == 3

def test_adjust_for_ace():
    hand = Hand()
    hand.add_card(Card('Hearts', 'Ace'))
    hand.add_card(Card('Hearts', '10'))
    hand.add_card(Card('Hearts', 'King'))
    assert hand.value == 21

if __name__ == "__main__":
    pytest.main(["-v", "unit_tests.py"])