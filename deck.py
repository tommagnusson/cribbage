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
    ACE = 1
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

    def points(self):
        if self in [Rank.JACK, Rank.QUEEN, Rank.KING]:
            return 10
        return self.value

    def __str__(self):
        if self.value == Rank.ACE.value:
            return 'A'
        if self.value == Rank.JACK.value:
            return 'J'
        if self.value == Rank.QUEEN.value:
            return 'Q'
        if self.value == Rank.KING.value:
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
    @staticmethod
    def shuffled():
        """
        Creates a shuffled deck with 52 standard cards.
        """
        cards = []
        # populate all the cards that exist in the deck...
        for suit in Suit:
            for rank in Rank:
                cards.append(Card(suit, rank))

        # shuffle them 
        random.shuffle(cards)
        return cards
