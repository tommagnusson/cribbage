from unittest import TestCase
from player import Player
from deck import Deck


class TestPlayer(TestCase):

    def test_deal(self):
        # Given a freshly made player
        p = Player()
        # When the player is dealt cards
        deal_cards = Deck.all_from_string(["3♣", "3♦"])
        p.deal(deal_cards)
        # Then both the player's hand and original hand are updated
        self.assertEqual(p.hand, deal_cards)
        self.assertEqual(p.original_hand, deal_cards)
