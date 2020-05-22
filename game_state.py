import random

from deck import Deck
from player import Player
from queue import Queue


class GameState:

    def __init__(self, inputFn=input):
        self.player1 = Player()
        self.player2 = Player()
        self.deck = Deck.shuffled()

        self.center_card = None
        self.played_stack = []
        self.crib = []
        self.phases = [self.re_shuffle, self.deal,
                       self.make_crib, self.cut, self.start]
        self.dealer = self.player1.id
        self.input = inputFn

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
        self.player1.hand = self.deal_hand()
        self.player2.hand = self.deal_hand()

    def prompt_crib(self, player):
        print("Lay away...")
        self.crib.append(self.select_card(player.hand))
        print("Lay away...")
        self.crib.append(self.select_card(player.hand))

    def select_card(self, cards):
        """
        Prompts the player to select a card from their hand
        Returns the selected card, which is removed from their hand.
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
                self.played_stack, the_count)
            player_queue.append(current_player)

    def filter_playable_cards(self, hand, count):
        needed = 31 - count
        for c in hand:
            if c.rank.points() <= needed:
                yield c

    straight = []
    matches = []

    def apply_score(self, played_stack, count):
        score = 0
        if count == 15 or count == 31:
            # Count is now 31 -> 2 points
            # Count is now 15 -> 2 points
            score += 2
        # Previous N are unordered straight (at least 3, three -> 3 points, four -> 4 points, etc)
        straight_queue_len = len(self.straight)
        if straight_queue_len == 0:
            # fill the straight queue
            self.straight.append(played_stack[-1])
        elif straight_queue_len == 1:
            # if it could be a straight then keep it going
            cmp = self.straight[0]
            diff = cmp - played_stack[-1]
            if abs(diff) == 1:
                # it's potentially a straight... keep the straight queue going
                self.straight.append(played_stack[-1])
                self.straight.sort()  # for easier checking
            else:
                # no straight, reset the queue
                self.straight.clear()
                # because it could still be this card in it, just reset the rest though
                self.straight.append(played_stack[-1])
        else:  # straight queue has at least 2 cards in it
            # check the bottom and top completion next
            bot = self.straight[0]
            top = self.straight[-1]
            cmp = self.played_stack[-1]
            bdiff = cmp - bot
            tdiff = cmp - top
            if abs(bdiff) == 1 or abs(tdiff) == 1:
                # add to the queue
                self.straight.append(cmp)
                # add points for the number of cards in the straight queue
                score += straight_queue_len + 1  # +1 bc of extra card added

        # Previous N are same rank (pair -> 2 points, triplet -> 6 points, quadruplet -> 12)
        matches_len = len(self.matches)
        if matches_len == 0:
            self.matches.append(played_stack[-1])  # add the last
        else:  # matches has at least one card, lets see if rank matches
            cmp = self.matches[0]
            if cmp.rank == played_stack[-1].rank:
                # add to the matches, add the points
                self.matches.append(played_stack[-1])
                # a[n] = n^2 + n is [2,6,12...]
                score += matches_len + matches_len**2
            else:
                self.matches.clear()
                # still might have the last played card to start somthing
                self.matches.append(played_stack[-1])

        return score
