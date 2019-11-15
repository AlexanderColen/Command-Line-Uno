class Card:
    # TODO Change to allow special cards
    value: -1
    colour: 'unassigned'

    def __init__(self, value, colour):
        self.value = value
        self.colour = colour.capitalize()

    def __str__(self):
        return '{0} {1}'.format(self.colour, self.value)
