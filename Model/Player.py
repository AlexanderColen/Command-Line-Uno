import random


class Player:
    name: 'Player'
    hand: []

    def __init__(self, name):
        self.name = name.capitalize()
        self.hand = []

        # Increase the pseudo-randomness by randomizing the seed.
        random.seed = random.randint(0, 10000)

    def __str__(self):
        return 'Name: {0} - Hand: {1}'.format(self.name, [c.__str__() for c in self.hand])

    # Choose a random playable card. If no card is playable, take the first card from the remaining deck.
    def choose_playable_card(self, top_card):
        playable = [c for c in self.hand if self.check_valid_move(top_card=top_card, chosen_card=c)]
        if len(playable) > 0:
            chosen_card = playable[random.randint(0, len(playable) - 1)]
            self.hand.remove(chosen_card)
            return chosen_card

        return None

    def add_card(self, card):
        self.hand.append(card)
        # TODO Implement sorting of hand.
        # self.hand.sort()

    # Checks if a chosen card is able to be played on the top card.
    @staticmethod
    def check_valid_move(top_card, chosen_card):
        return top_card.value == chosen_card.value or top_card.colour == chosen_card.colour

