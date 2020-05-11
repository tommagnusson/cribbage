from enum import Enum
import random

class Suit(Enum):
    HEARTS = '♥'
    SPADES = '♠'
    DIAMONDS = '♦'
    CLUBS = '♣'

    def __str__(self):
        return self.value

class Rank(Enum):
    ACE = 0
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __str__(self):
        if self.value == 0:
            return 'A'
        if self.value == 11: 
            return 'J'
        if self.value == 12: 
            return 'Q'
        if self.value == 13: 
            return 'K'

        return str(self.value)

    def compare(self, r2):
        return self.value - r2.value

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __repr__(self):
        return str(self.rank) + str(self.suit)

class Deck:
    def __init__(self):
        self.cards = []
        # populate all the cards that exist in the deck...
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))

        # shuffle them 
        random.shuffle(self.cards)

print(Deck().cards)
