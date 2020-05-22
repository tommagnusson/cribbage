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
    
    def __sub__(self, other):
        return self.value - other.value 
    
    @staticmethod
    def fromString(s):
        """
        From <number>|(J|Q|K|A) format to class
        """
        try:
            return Rank(int(s))
        except ValueError:
            # check for one of J, Q, K, A
            if s == 'A':
                return Rank(1)
            if s == 'J':
                return Rank(11)
            if s == 'Q':
                return Rank(12)
            if s == 'K':
                return Rank(13)
        raise ValueError(f"Invalid string: {s}")

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    @staticmethod
    def from_string(s):
        """
        Takes a card formatted as <rank><suit> and creates a card
        """
        suit = s[-1]
        rank = s[:-1]
        return Card(Suit(suit), Rank.fromString(rank))

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __repr__(self):
        return str(self.rank) + str(self.suit)
    
    def __sub__(self, other):
        return self.rank - other.rank 

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == self.rank

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

    @staticmethod
    def all_from_string(ss):
        """
        Convenience method for Card.from_string over a list of card strings
        """
        return [Card.from_string(c) for c in ss]
