from __future__ import annotations

from random import choice

from cubirds import Game, Bird, Stage, Side, Place, Fly, Buy, Pass


def show_table(table):
    print('Table:')
    for row in table.table:
        print('\t' + ' '.join([repr(b) for b in row]))


def show_player(player):
    print(f'Player #{player.id} (current turn):')
    print('\tHand:', player.hand)  # TODO: could use flatten deck here
    print('\tCollection:', player.collection)


# TODO: code into Game what is visible and isn't?
def show_game(game):     # TODO: add to Game?
    # TODO: only for 2 player (for now)
    #print(game)
    #print()

    print("=" * 80)
    print(f"Player #{game.current_player.id}'s turn")

    show_table(game.table)
    print(f'Draw: {len(game.draw)} cards')
    print(f'Discard: {len(game.discard)} cards')

    opponent = (game.current_player.id + 1) % game.num_players
    print(f'Player #{opponent} (opponent) Collection:', game.players[opponent].collection)

    if game.stage == Stage.PLACE:
        print('Possible Action: You can place birds into the table')
    elif game.stage == Stage.BUY_OR_PASS:
        print('Possible Action: You can buy 2 cards or pass')
    elif game.stage == Stage.FLY_OR_PASS:
        print('Possibly Action: You can let a flock fly or pass')

    show_player(game.current_player)


def _ask_species(game):
    species = list(game.current_player.hand.get_species())
    species_str = ''.join(repr(b) for b in species)

    while True:
        result = input(f'Choose species ({species}, default={species[0]!r}): ').upper()
        if result in species_str:
            # print(result)
            break
        else:
            print(f'Error: result not in {species}')

    if result == '':
        # TODO: why the slowdown before this option
        print(repr(species[0]))
        return species[0]
    else:
        bird = [b for b in Bird if repr(b) == result]
        assert len(bird) == 1
        return bird[0]


def _ask_row(game):
    while True:
        try:
            result = input(f'Choose row (0-3, default=0): ')

            if result == '':
                print(0)
                return 0

            result = int(result)
            if result < 0 or result > 3:
                print('Error: result is not in (0-3)')
                continue

            return result
        except ValueError:
            print('Error: result is not in (0-3)')


def _ask_side(game):
    while True:
        result = input(f'Choose side (R: Right/L: Left, default=R): ').upper()

        if result == '':
            print(repr(Side.RIGHT))
            return Side.RIGHT
        elif result == 'L':
            return Side.LEFT
        elif result == 'R':
            return Side.RIGHT
        else:
            print('Error: result not in (R/L)')


def _ask_buy_or_pass(game):
    while True:
        result = input(f'Choose Buy (B) or Pass (P) (default=P): ').upper()

        if result == '':
            p = Pass()
            print(p)
            return p
        elif result == 'B':
            return Buy()
        elif result == 'P':
            return Pass()
        else:
            print('Error: result is not (B/P)')


# TODO: test this
def _ask_fly_species(game):
    flocks = list(game.current_player.hand.get_flocks())

    if len(flocks) == 1:
        print(f'Since there is only a single flock, {flocks[0]} was chosen')
        return flocks[0]
    else:
        flocks_str = ''.join(repr(b) for b in flocks)

        while True:
            result = input(f'Choose flock ({flocks}, default={flocks[0]!r}): ').upper()

            if result == '':
                print(repr(flocks[0]))
                return flocks[0]
            elif result in flocks_str:
                bird = [b for b in Bird if repr(b) == result]
                assert len(bird) == 1
                return bird[0]
            else:
                print(f'Error: result not in {flocks}')


def _ask_fly_or_pass(game):
    while True:
        result = input(f'Choose Fly (F) or Pass (P) (default=P): ').upper()

        if result == '':
            p = Pass()
            print(p)
            return p
        elif result == 'F':
            return Fly(_ask_fly_species(game))
        elif result == 'P':
            return Pass()
        else:
            print('Error: result is not (F/P)')


def ask_move(game):
    while True:
        if game.stage == Stage.PLACE:
            #print('Place Move:')
            bird = _ask_species(game)
            row = _ask_row(game)
            side = _ask_side(game)

            if (move := Place(bird, row, side)) in game.get_legal_moves():
                return move
            else:
                print('Error: move is not a legal move')
        elif game.stage == Stage.BUY_OR_PASS:
            return _ask_buy_or_pass(game)
        elif game.stage == Stage.FLY_OR_PASS:
            return _ask_fly_or_pass(game)


def main():
    game = Game(2)

    while not game.is_endgame():
        if game.current_player.id == 0:
            show_game(game)
            move = ask_move(game)
            print(move)
            game.play(move)
        else:
            show_game(game)
            # TODO: turn get_species into @property species
            move = choice(list(game.get_legal_moves()))
            print(move)
            game.play(move)


if __name__ == '__main__':
    main()
