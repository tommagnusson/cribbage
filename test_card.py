from unittest import TestCase
from deck import Card, Rank, Suit

class TestCard(TestCase):

    def test_from_string(self):
        # Given a few cards are formatted as strings...
        qd = "Q♦"
        fs = "4♠"
        jc = "J♣" 
        ah = "A♥"
        kc = "K♣"
        # When each is converted into Card instances...
        QD = Card.from_string(qd)
        FS = Card.from_string(fs)
        JC = Card.from_string(jc)
        AH = Card.from_string(ah)
        KC = Card.from_string(kc)
        # Then the conversion is correct
        self.assertEqual(QD, Card(Suit.DIAMONDS, Rank.QUEEN))
        self.assertEqual(FS, Card(Suit.SPADES, Rank.FOUR))
        self.assertEqual(JC, Card(Suit.CLUBS, Rank.JACK))
        self.assertEqual(AH, Card(Suit.HEARTS, Rank.ACE))
        self.assertEqual(KC, Card(Suit.CLUBS, Rank.KING))
    
    def test_ten_rank_from_string(self):
        ten_of_spades = "10♠"
        ts = Card.from_string(ten_of_spades)
        self.assertEqual(ts, Card(Suit.SPADES, Rank.TEN))
