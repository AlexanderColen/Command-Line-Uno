from Model.Card import Card
import random
import sys


# Set up the deck for play, giving a parameter whether to include special cards or not.
def setup_deck(include_specials=False):
    deck = []
    colours = ['blue', 'red', 'green', 'yellow']

    for value in range(0, 10):
        for colour in colours:
            deck.append(Card(value, colour))
            # Make sure to generate 2 of every numeric card that isn't a 0.
            if value != 0:
                deck.append(Card(value, colour))

    if include_specials:
        # TODO Generate special cards.
        raise NotImplementedError('This functionality has yet to be implemented.')

    return deck


# Checks if a chosen card is able to be played on the top card.
def check_valid_move(top_card, chosen_card):
    return top_card.value == chosen_card.value or top_card.colour == chosen_card.colour


if __name__ == '__main__':
    print('Command Line Uno | Copyright (C) 2019 | Alexander Colen')
    print('\nSetting up the deck...')
    d = setup_deck(include_specials=False)

    # Increase the pseudo-randomness by randomizing the seed.
    random.seed = random.randint(0, 10000)

    # Shuffle the deck to increase randomness.
    random.shuffle(d)

    print('\nGenerating card validity checks...')
    # Generate 1000 card checks.
    for i in range(1000):
        d_copy = d.copy()
        top = d_copy[random.randint(0, len(d_copy) - 1)]
        d_copy.remove(top)
        hand = []
        for j in range(0, 10):
            random_card = d_copy[random.randint(0, len(d_copy) - 1)]
            hand.append(random_card)
            d_copy.remove(random_card)

        playable = []
        for card in hand:
            if check_valid_move(top_card=top, chosen_card=card):
                playable.append(card)

        print('Top card: {0} - Cards able to play: {1}'.format(top, [c.__str__() for c in playable]))

    if 'check' in sys.argv:
        while True:
            print('\nCustom card validity checking...')
            top_colour = input('\nEnter the colour of the top card: ')
            top_value = input('Enter the value of the top card: ')

            chosen_colour = input('Enter the colour of your chosen card: ')
            chosen_value = input('Enter the value of your chosen card: ')

            top = Card(top_value, top_colour)
            chosen = Card(chosen_value, chosen_colour)
            validity = check_valid_move(top_card=top, chosen_card=chosen)
            print('Top card: {0} - Chosen card: {1} - Able to play: {2}\n'.format(top, chosen, validity))

            if input('Stop manual checking? (Y/N): ') in ['Y', 'y', 'Yes', 'yes', 'YES']:
                break

    # TODO: Make the game playable vs one or more AI opponents.
