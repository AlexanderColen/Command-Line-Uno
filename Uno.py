from Model.Card import Card
from Model.Player import Player
from collections import deque
import random
import sys
import time


# Set up the deck for play, giving a parameter whether to include special cards or not.
def setup_deck(include_specials=False):
    print('\nSetting up the deck...')
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


# Generate all the players for this game.
def generate_players(player_name, count):
    print('\nGenerating players...')
    generated_players = [Player(player_name)]

    for i in range(1, count + 1):
        generated_players.append(Player('AI {0}'.format(i)))

    return generated_players


# Distributes cards to all the players and returns the remaining deck.
def distribute_cards(deck, all_players, amount):
    print('\nDistributing cards...')
    for i in range(amount):
        for p in all_players:
            a_card = deck[random.randint(0, len(deck) - 1)]
            p.add_card(a_card)
            deck.remove(a_card)

    return deck


# Take the top card from the remaining deck.
def take_card(deck, played):
    if len(deck) == 0:
        deck = random.shuffle(played.copy())
        played = []

    taken_card = deck[0]
    deck.remove(taken_card)

    return deck, taken_card, played


if __name__ == '__main__':
    print('Command Line Uno | Copyright (C) 2019 | Alexander Colen')
    d = setup_deck(include_specials=False)

    # Increase the pseudo-randomness by randomizing the seed.
    random.seed = random.randint(0, 10000)

    # Shuffle the deck to increase randomness.
    random.shuffle(d)

    if 'test' in sys.argv:
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
                if top.value == card.value or top.colour == card.colour:
                    playable.append(card)

            print('Top card: {0} - Cards able to play: {1} - Full hand: {2}'
                  .format(top, [c.__str__() for c in playable], [c.__str__() for c in hand]))

    if 'check' in sys.argv:
        while True:
            print('\nCustom card validity checking...')
            top_colour = input('\nPlease enter the colour of the top card.\n> ')
            top_value = input('Please enter the value of the top card.\n> ')

            chosen_colour = input('Please enter the colour of your chosen card.\n> ')
            chosen_value = input('Please enter the value of your chosen card.\n> ')

            top = Card(top_value, top_colour)
            chosen = Card(chosen_value, chosen_colour)
            print('Top card: {0} - Chosen card: {1} - Able to play: {2}\n'
                  .format(top, chosen, top.value == chosen.value or top.colour == chosen.colour))

            if input('Stop manual checking? (Y/N)\n> ') in ['Y', 'y', 'Yes', 'yes', 'YES']:
                break

    if 'play' in sys.argv:
        play = True
    else:
        play = input('Would you like to play a game of Uno? [Y/N]\n> ') in ['Y', 'y', 'Yes', 'yes', 'YES']

    if play:
        print('\nSetting up playable game of Uno...')
        name = input('What should I call you?\n> ')
        while play:
            computer_count = int(input('How many computers do you want to play against? (Maximum of 9 opponents)\n> '))
            if computer_count > 9:
                print('Maximum allowed number of players exceeded. Setting total amount of AI to 9.')
                computer_count = 9
            elif computer_count < 1:
                print('You need at least two players to play Uno. Setting total amount of AI to 1.')
                computer_count = 1
            players = deque(generate_players(player_name=name, count=computer_count))

            remaining_deck = distribute_cards(deck=d.copy(), all_players=players, amount=7)
            for p in players:
                print(p)

            # Rotate the players array randomly to see whose turn it is!
            players.rotate(random.randint(0, 100))

            print('\nLet the games begin!')
            print('{0} gets to start the game.'.format(players[0].name))

            # Start the actual game.
            game_over = False
            current_card = remaining_deck[0]
            remaining_deck.remove(current_card)
            played_cards = []
            while not game_over:
                print('\nThe current top card is a {0}.'.format(current_card))
                print("It is {0}'s turn.".format(players[0].name))

                if players[0].name != name.capitalize():
                    time.sleep(2)
                    played_card = players[0].choose_playable_card(top_card=current_card)
                    if played_card:
                        played_cards.append(current_card)
                        current_card = played_card
                        print('{0} played the {1}!'.format(players[0].name, played_card))
                    else:
                        # Needs to draw a card.
                        remaining_deck, new_card, played_cards = take_card(remaining_deck, played_cards)
                        players[0].add_card(new_card)
                        print('{0} drew a card.'.format(players[0].name))
                else:
                    print('Your hand looks like this: {0}'.format([c.__str__() for c in players[0].hand]))
                    playable = False
                    for card in players[0].hand:
                        if current_card.value == card.value or current_card.colour == card.colour:
                            playable = True
                            break

                    if playable:
                        choosing = True
                        while choosing:
                            card_index = int(input('\nChoose the number of the card that you want to play from your hand:\n> ')) - 1
                            chosen_card = players[0].hand[card_index]
                            correct = input('Are you sure you want to play {0}? [Y/N]\n> '
                                            .format(chosen_card)) in ['Y', 'y', 'Yes', 'yes', 'YES']
                            if correct:
                                if players[0].check_valid_move(top_card=current_card, chosen_card=chosen_card):
                                    played_cards.append(current_card)
                                    current_card = chosen_card
                                    choosing = False
                                    players[0].hand.remove(current_card)
                                    # TODO Implement sorting of hand.
                                    # players[0].hand.sort()
                                    print('{0} played the {1}!'.format(players[0].name, chosen_card))
                                else:
                                    print('Playing this card would be an illegal move!')
                                    print('You cannot play a {0} on a {1}'.format(chosen_card, current_card))
                    else:
                        # Needs to draw a card.
                        remaining_deck, new_card, played_cards = take_card(remaining_deck, played_cards)
                        players[0].add_card(new_card)
                        print('You drew a {0}.'.format(new_card))

                print('{0} has {1} cards remaining.'.format(players[0].name, len(players[0].hand)))

                # Check for win condition.
                if len(players[0].hand) == 0:
                    print('{0} won this game!'.format(players[0].name))
                    game_over = True
                elif len(players[0].hand) == 1:
                    print('\n{0} yells UNO!'.format(players[0].name))

                # Rotate the deque so it's the next player's turn.
                players.rotate()

            play = input('Would you like to play another game? [Y/N]\n> ') in ['Y', 'y', 'Yes', 'yes', 'YES']
