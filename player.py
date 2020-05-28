class Player:

    # increments to identify players
    identifier = 1

    def __init__(self):
        self.hand = []  # cards, the active ones meant to be mutated
        # meant to be a read only copy of the original hand (for scoring after a round)
        self.original_hand = []
        self.score = 0  # score in points
        self.id = Player.identifier
        Player.identifier += 1

    def __repr__(self):
        return f"Player {self.id}: [{','.join(str(h) for h in self.hand)}] | {self.score}"

    def __str__(self):
        return f"Player {self.id}: [{','.join(str(h) for h in self.hand)}] | {self.score}"
