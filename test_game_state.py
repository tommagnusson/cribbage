import unittest
from unittest.mock import MagicMock
from game_state import GameState
import random
from deck import Card, Rank, Suit, Deck


class TestGameState(unittest.TestCase):

    def setUp(self):
        """
        Creates the following deck
        [Q♦, J♣, 4♦, 10♣, 8♠, K♠, 6♠, 10♠,
         8♦, Q♥, 5♣, 8♥, 10♥, 8♣, 4♠, J♠, 
         9♣, 5♥, 5♦, 2♥, A♣, 2♠, 7♦, 6♦, 
         2♦, K♥, 7♠, 7♣, 6♣, A♠, 3♦, A♥, 
         K♦, 3♠, J♦, 4♣, 2♣, 9♥, J♥, K♣, 
         3♣, 9♠, 10♦, 9♦, Q♠, 3♥, 7♥, Q♣, 
         A♦, 6♥, 5♠, 4♥]
        """
        random.seed(123)

    def test_deal_hand(self):
        # Given a normal game state
        gs = GameState()
        # When the deal happens
        gs.deal()
        # Then the first player gets the first 6 cards
        expected_player1_hand = Deck.all_from_string(
            ["Q♦", "J♣", "4♦", "10♣", "8♠", "K♠"])
        self.assertEqual(gs.player1.hand, expected_player1_hand)
        # and the second player get the second 6 cards
        expected_player2_hand = Deck.all_from_string(
            ["6♠", "10♠", "8♦", "Q♥", "5♣", "8♥", ])
        self.assertEqual(gs.player2.hand, expected_player2_hand)

    def test_prompt_crib(self):
        # Given a normal game state
        # players always lay away 0th card (first two in this case)
        firstCardLay = MagicMock(return_value=0)
        gs = GameState(inputFn=firstCardLay)
        gs.deal()
        # When players lay their cards away...
        gs.make_crib()
        # Then the crib contains the laid off cards
        self.assertListEqual(
            gs.crib, Deck.all_from_string(["Q♦", "J♣", "6♠", "10♠"]))

    def test_select_card_with_invalid_index(self):
        # Given a player with a hand of 6 cards (indicies 0 to 5)
        invalid_card_lay = MagicMock(side_effect=["6", "0"])
        gs = GameState(inputFn=invalid_card_lay)
        gs.deal()
        # When the player selects an index out of bound, and then the first card
        expected_card = gs.player1.hand[0]
        card = gs.select_card(gs.player1.hand)
        # Then the first card is returned
        self.assertEqual(card, expected_card)

    def test_select_card_with_non_int(self):
        # Given a player with a hand of 6 cards
        non_int_lay = MagicMock(side_effect=["non_int", "0"])
        gs = GameState(inputFn=non_int_lay)
        gs.deal()
        # When the player provides a non integer instead of an index, and then the first card
        expected_card = gs.player1.hand[0]
        card = gs.select_card(gs.player1.hand)
        # Then the first card is returned
        self.assertEqual(card, expected_card)

    def test_filter_playable_cards(self):
        # Given a count of 25
        count = 25
        gs = GameState()
        # and a hand with some cards that are less than 7 points
        hand = Deck.all_from_string(
            ["Q♦", "J♣", "4♦", "10♣", "8♠", "K♠", "6♠"])
        # When the playable cards are filtered
        filtered = list(gs.filter_playable_cards(hand, count))
        # Then all the cards returned are less than 7 points
        expected_filtered = Deck.all_from_string(["4♦", "6♠"])
        self.assertEqual(filtered, expected_filtered)
