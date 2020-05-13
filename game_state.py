import random

from deck import Deck
from player import Player


class GameState:

    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.deck = Deck.shuffled()

        self.center_card = None
        self.played_stack = []
        self.crib = []
        self.phases = [self.re_shuffle, self.deal, self.make_crib, self.cut, self.start]
        self.dealer = self.player1.id

    def play(self):
        print('Welcome to Cribbage :)')
        while self.player1.score <= 121 and self.player2.score <= 121:
            for i in range(len(self.phases)):
                self.phases[i]()

    def re_shuffle(self):
        self.deck = Deck.shuffled()

    def deal_hand(self):
        return [self.deck.pop(ind) for ind in range(6)]

    def deal(self):
        self.player1.hand = self.deal_hand()
        self.player2.hand = self.deal_hand()

    def prompt_crib(self, player):
        print(player)
        card = input('Please lay away 1 card. which card would you like to lay away? (enter the index of the card - first card is 0)')

        self.crib.append(player.hand.pop(int(card)))

        print(player)
        card = input('Please lay away another card. which card would you like to lay away? (enter the index of the card - first card is 0)')
        self.crib.append(player.hand.pop(int(card)))

    def make_crib(self):
        print('Cards should now be layed away into the crib. Please pass the game to player 1')
        print('Player 1:')
        self.prompt_crib(self.player1)

        print('Please pass the game to player 2')
        print('Player 2:')
        self.prompt_crib(self.player2)

        print('The crib has been created.')

    def cut(self):
        cut_number = int(input(f'Player {self.player1.id}, please select a number between 5 and {len(self.deck)} to cut the deck'))
        self.center_card = self.deck[cut_number]
        print(f'The center card is {self.center_card}')

    def start(self):
        print('let the game begin')
        all_go = False
        limit_reached = False
        # TODO: player 2 should not always go first
        player_queue = [self.player2, self.player1]
        the_count = 0
        while not all_go or limit_reached:
            print(f"the count is {the_count}")
            current_player = player_queue.pop(0)
            print(current_player)
            # TODO: check if the current player has to "go" / filter invalid cards to play when gathering input
            card_played = current_player.hand.pop(int(input("Play a card from your hand (enter the index of the card - first card is 0)")))
            self.played_stack.append(card_played)
            print(f"{card_played} was played.")
            the_count += card_played.rank.points()
            # check if the count has been reached, add appropriate points scoring-wise
            player_queue.append(current_player)
