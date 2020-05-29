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

    def test_filter_playable_cards(self):
        # Given a count of 31 (too many)
        count = 31
        gs = GameState()
        # and a hand with cards
        hand = Deck.all_from_string(
            ["Q♦", "J♣", "4♦", "10♣", "8♠", "K♠", "6♠"])
        # When the playable cards are filtered
        filtered = list(gs.filter_playable_cards(hand, count))
        # Then no cards are played
        expected = []
        self.assertEqual(filtered, expected)

    def test_check_straight_adds_single_card(self):
        # Given an empty straight list
        gs = GameState()
        self.assertEqual(gs.straight, [])
        # When the player plays a new card and the straight is checked
        played_card = Card.from_string("Q♦")
        score = gs.check_straight(played_card)
        # Then no score is returned and that card is in the straight list
        expected_score = 0
        expected_straight_list = [played_card]
        self.assertEqual(score, expected_score)
        self.assertEqual(gs.straight, expected_straight_list)

    def test_check_straight_adds_rising_pair(self):
        # Given a straight list with a card
        gs = GameState()
        gs.straight = [Card.from_string("Q♦")]
        # When the player plays a new card that is one rank below the existing card, with a different suit (suit doesn't matter)
        played_card = Card.from_string("J♣")
        score = gs.check_straight(played_card)
        # Then no score is returned, and both cards are still in the straight list, sorted in ascending order
        expected_score = 0
        expected_straight_list = [played_card, Card.from_string("Q♦")]
        self.assertEqual(score, expected_score)
        self.assertEqual(gs.straight, expected_straight_list)

    def test_check_straight_adds_triple(self):
        # Given a straight list with a rising pair
        gs = GameState()
        starting_straight = [Card.from_string("3♠"), Card.from_string("4♠")]
        gs.straight = starting_straight
        # When the player plays a new card that is one rank below the lowest card in the pair
        played_card = Card.from_string("2♦")
        score = gs.check_straight(played_card)
        # Then the score returned is 3, and the straight list is ascending
        expected_score = 3
        expected_straight_list = [
            played_card, Card.from_string("3♠"), Card.from_string("4♠")]
        self.assertEqual(score, expected_score)
        self.assertEqual(gs.straight, expected_straight_list)

    def test_check_straight_adds_quad(self):
        # Given a straight list with a triple
        gs = GameState()
        starting_straight = Deck.all_from_string(["2♦", "3♠", "4♠"])
        gs.straight = starting_straight
        # When the player plays a new card that fits the straight
        played_card = Card.from_string("A♦")
        score = gs.check_straight(played_card)
        # Then the score returned is 4, and the straight list is ascending
        expected_score = 4
        expected_straight_list = Deck.all_from_string(["A♦", "2♦", "3♠", "4♠"])
        self.assertEqual(score, expected_score)
        self.assertEqual(gs.straight, expected_straight_list)

    def test_check_straight_breaks_straight(self):
        # Given a straight list with a triple
        gs = GameState()
        starting_straight = Deck.all_from_string(["2♦", "3♠", "4♠"])
        gs.straight = starting_straight
        # When the player plays a new card that break the straight
        played_card = Card.from_string("6♦")
        score = gs.check_straight(played_card)
        # Then the score returned is 0, and the straight list contains only that newly played card
        expected_score = 0
        expected_straight_list = Deck.all_from_string(["6♦"])
        self.assertEqual(score, expected_score)
        self.assertEqual(gs.straight, expected_straight_list)

    def test_check_match_single_played_card(self):
        # Given an empty match list
        gs = GameState()
        starting_matches = []
        gs.matches = starting_matches
        # When the player plays a new card
        played_card = Card.from_string("3♣")
        score = gs.check_match(played_card)
        # Then the score returned is 0, and the match list contains that one card
        expected_score = 0
        expected_matches_list = [played_card]
        self.assertEqual(score, expected_score)
        self.assertEqual(gs.matches, expected_matches_list)

    def test_check_match_two_matched_cards(self):
        # Given a match list with one card
        gs = GameState()
        starting_matches = [Card.from_string("3♣")]
        gs.matches = starting_matches
        # When the player plays a card with the same rank
        played_card = Card.from_string("3♦")
        score = gs.check_match(played_card)
        # Then the score returned is 2, and the match list contains the played card
        expected_score = 2
        expected_matches_list = Deck.all_from_string(["3♣", "3♦"])
        self.assertEqual(score, expected_score)
        self.assertEqual(gs.matches, expected_matches_list)

    def test_check_match_break_card(self):
        # Given a match list with one card
        gs = GameState()
        starting_matches = [Card.from_string("K♦")]
        gs.matches = starting_matches
        # When the player plays a card with a different rank
        played_card = Card.from_string("A♦")
        score = gs.check_match(played_card)
        # The the score returned is 0, and the match contains just the newly played card
        expected_score = 0
        expected_matches_list = [played_card]
        self.assertEqual(score, expected_score)
        self.assertEqual(gs.matches, expected_matches_list)

    def test_score_meld_15(self):
        # Given a meld that adds up to 15
        gs = GameState()
        meld = (Card.from_string("5♦"), Card.from_string("J♣"))
        # When the meld is scored
        score = gs.score_meld(meld)
        # The returned score is 2
        self.assertEqual(score, 2)

    def test_score_meld_nothing(self):
        # Given a meld that has no value
        gs = GameState()
        meld = (Card.from_string("4♦"), Card.from_string("J♣"))
        # When the meld is scored
        score = gs.score_meld(meld)
        # The returned score is 0
        self.assertEqual(score, 0)

    def test_score_meld_straight(self):
        # Given a meld that has a straight of three cards of different suits
        gs = GameState()
        meld = (Card.from_string("3♦"), Card.from_string(
            "2♣"), Card.from_string("4♦"))
        # When the meld is scored
        score = gs.score_meld(meld)
        # The returned score is 3
        self.assertEqual(score, 3)

    def test_score_meld_match_triplet(self):
        # Given a meld that has a three of a kind
        gs = GameState()
        meld = tuple(Deck.all_from_string(["2♠", "2♦", "2♥"]))
        # When the meld is scored
        score = gs.score_meld(meld)
        # The returned score is 2 + 2 + 2 = 6
        self.assertEqual(score, 6)

    def test_score_meld_match_quad(self):
        # Given a meld that has a three of a kind
        gs = GameState()
        meld = tuple(Deck.all_from_string(["2♠", "2♦", "2♥", "2♣"]))
        # When the meld is scored
        score = gs.score_meld(meld)
        # The returned score is 12
        self.assertEqual(score, 12)


"""
♠♦♥♣ 
"""
