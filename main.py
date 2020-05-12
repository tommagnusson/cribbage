from Player import Player
from Deck import Deck

player1 = Player()
player2 = Player()

deck = Deck.shuffled()

player1.hand = deck[:5]
player2.hand = deck[5:10]
print(player1)
print(player2)

# TODO(): event loop for turns and structure of a round
