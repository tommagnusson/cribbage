import random

from deck import Deck
from player import Player
from queue import Queue


class GameState:

    def __init__(self, inputFn=input):
        self.player1 = Player()
        self.player2 = Player()
        self.deck = Deck.shuffled()
        self.played_by_player = {}

        self.center_card = None
        self.played_stack = []
        self.crib = []
        self.phases = [self.re_shuffle, self.deal,
                       self.make_crib, self.cut, self.start]
        self.dealer = self.player1.id
        self.input = inputFn
        self.straight = []  # used for straight detection in play phase
        self.matches = []  # used for match detection in play phase

    def play(self):
        print('Welcome to Cribbage :)')
        while self.player1.score <= 121 and self.player2.score <= 121:
            for i in range(len(self.phases)):
                self.phases[i]()

    def re_shuffle(self):
        self.deck = Deck.shuffled()

    def deal_hand(self):
        return [self.deck.pop(0) for ind in range(6)]

    def deal(self):
        self.player1.deal(self.deal_hand())
        self.player2.deal(self.deal_hand())

    def prompt_crib(self, player):
        print("Lay away...")
        self.crib.append(self.select_card(player.hand))
        print("Lay away...")
        self.crib.append(self.select_card(player.hand))

    def select_card(self, cards):
        """
        Prompts the player to select a card from the cards provided
        Returns the selected card, which is removed from the list of cards provided
        """
        idx = -1  # should not be inital value
        while True:
            print("Please select a card by index:")
            inpt = self.input(list(enumerate(cards)))
            try:
                idx = int(inpt)
            except ValueError:
                print(f"'{inpt}' is not a valid index.")
            if idx < 0 or idx >= len(cards):
                print(f"The index {idx} is not available.")
            else:
                break
        assert idx != -1  # make sure it's not initial value
        return cards.pop(idx)

    def make_crib(self):
        print(
            'Cards should now be layed away into the crib. Please pass the game to player 1')
        print('Player 1:')
        self.prompt_crib(self.player1)

        print('Please pass the game to player 2')
        print('Player 2:')
        self.prompt_crib(self.player2)

        print('The crib has been created.')

    def cut(self):
        print("Please select a number to cut the deck by...")
        print(f"The center card is {self.select_card(self.deck)}")

    def start(self):
        print('let the game begin')
        all_go = False
        limit_reached = False
        # TODO: player 2 should not always go first
        player_queue = [self.player2, self.player1]
        the_count = 0
        while True:
            print(f"the count is {the_count}")
            current_player = player_queue.pop(0)
            print(current_player)
            playable_cards = list(self.filter_playable_cards(
                current_player.hand, the_count))
            if len(playable_cards) == 0:
                print("GO")
                # TODO: the other player gets a point
                break
            print(f"Play any of these: {playable_cards}")
            # TODO: sanitize input from user
            card_played = current_player.hand.pop(int(self.input(
                "Play a card from your hand (enter the index of the card - first card is 0)")))
            self.played_stack.append(card_played)
            print(f"{card_played} was played for {card_played.rank.points()} points.")
            the_count += card_played.rank.points()
            current_player.score += self.apply_score(
                card_played, the_count)
            player_queue.append(current_player)

    def filter_playable_cards(self, hand, count):
        needed = 31 - count
        for c in hand:
            if c.rank.points() <= needed:
                yield c

    def check_landed_15_or_31(self, count):
        if count == 15 or count == 31:
            # Count is now 31 -> 2 points
            # Count is now 15 -> 2 points
            return 2
        return 0

    def check_straight(self, played_card):
        straight_len = len(self.straight)
        if straight_len == 0:
            # fill the straight list
            self.straight.append(played_card)
        else:  # straight queue has at least 1 card in it
            # check the bottom and top completion next
            bot = self.straight[0]
            top = self.straight[-1]
            cmp = played_card
            bdiff = cmp - bot
            tdiff = cmp - top
            if abs(bdiff) == 1 or abs(tdiff) == 1:
                # add to the list
                self.straight.append(cmp)
                self.straight = sorted(
                    self.straight, key=lambda c: c.rank.value)
                # add points for the number of cards in the straight list
                # unless there are only two cards in there
                pts = len(self.straight)
                return pts if pts > 2 else 0
            else:
                # straight broken, clear straight list
                # add played card because it might be part of a subsequent straight
                self.straight.clear()
                self.straight.append(played_card)
        return 0

    def check_match(self, played_card):
        matches_len = len(self.matches)
        if matches_len == 0:
            self.matches.append(played_card)  # add the last
        else:  # matches has at least one card, lets see if rank matches
            cmp = self.matches[0]
            if cmp.rank == played_card.rank:
                # add to the matches, add the points
                self.matches.append(played_card)
                # a[n] = n^2 + n is [2,6,12...]
                return matches_len + matches_len**2
            else:
                self.matches.clear()
                # still might have the last played card to start somthing
                self.matches.append(played_card)
        return 0

    def apply_score(self, played_card, count):
        score += self.check_landed_15_or_31(count)
        # Previous N are unordered straight (at least 3, three -> 3 points, four -> 4 points, etc)
        score += self.check_straight(played_card)
        # Previous N are same rank (pair -> 2 points, triplet -> 6 points, quadruplet -> 12)
        score += self.check_match(played_card)
        return score
