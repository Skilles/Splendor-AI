from operator import attrgetter

import util


def do_action(game):
    output = game.network.activate(get_input(game))
    # # [take_black, take_red, take_green, take_blue, take_white, buy, reserve]
    # [take_tokens, buy, reserve]
    # take_tokens
    # buy = index
    # reserve = index
    take_tokens = output[0]
    buy = output[1]
    reserve = output[2]
    cards = []
    action = 'buy'
    for row in game.board:
        for card in row:
            cards.append(card)
    can_buy = [card for card in cards if game.player.can_buy(card)]
    op_can_buy = [card for card in cards if game.opponent.can_buy(card)]
    if buy > 0.3 and not game.player.has_taken() and len(can_buy) > 0:
        card = max(can_buy, key=attrgetter('points'))
        game.player.buy(card)
        return action
    # TODO: use player.can_take(token)
    if take_tokens > 0:
        action = 'take tokens'
        color = None
        if take_tokens < 0.2 and len(util.get_colors(game.tokens, 'black')) > 0:
            color = 0
        elif take_tokens < 0.4 and len(util.get_colors(game.tokens, 'red')) > 0:
            color = 1
        elif take_tokens < 0.6 and len(util.get_colors(game.tokens, 'green')) > 0:
            color = 2
        elif take_tokens < 0.8 and len(util.get_colors(game.tokens, 'blue')) > 0:
            color = 3
        elif take_tokens <= 1 and len(util.get_colors(game.tokens, 'white')) > 0:
            color = 4
        if color:
            game.player.take_token(color=util.index_to_color(color))
            return action
    if reserve > 0.3 and not game.player.has_taken() and len(game.player.reserved) < 3:
        action = 'reserve'
        if len(op_can_buy) > 0:
            card = max(op_can_buy, key=attrgetter('points'))
        else:
            card = min([card for card in cards if card.level != 0], key=lambda card: sum(card.price))
        game.player.reserve(card)
        return action
    action = 'none'
    return action


def can_buy_binary(board, player):
    output = ''
    for row in board:
        for card in row:
            if player.can_buy(card):
                output += '1'
            else:
                output += '0'
    return int(output)


def tokens_binary(tokens):
    output = ''
    for i in range(0, 5):
        color = util.index_to_color(i)
        colors = util.get_colors(tokens, color)
        output += str(len(colors))
    return int(output)


def price_binary(card=None, noble=None):
    if card and noble:
        raise Exception('Card or noble, not both!')
    if card:
        output = ''
        for i in range(0, 5):
            output += str(card.price[i])
        output += str(card.points)
        output += str(color_to_index(card.color))
    else:
        output = ''
        for i in noble.price:
            output += str(i)
    return int(output)


def color_to_index(color):
    if color == 'black':
        return 0
    elif color == 'red':
        return 1
    elif color == 'green':
        return 2
    elif color == 'blue':
        return 3
    elif color == 'white':
        return 4
    elif color == 'yellow':
        return 5


# This function takes a game and returns the inputs for its player In the future this will return a tuple of the
# player and opponent's inputs
# INPUTS: (noble1, noble2, noble3, row1card1, row1card2, row1card3,
# row2card1, row2card2, row2card3, row3card1, row3card2, row3card3, can_buy, opponent_can_buy, board.tokens)
# [333, 44000, 33300, 370051, 743, 3700050, 7042, 303214, 600031, 2030310, 5023, 1121004, 1001304, 1310000, 300002, 0, 0, 77777]
def get_input(game):
    output = []
    can_buy = can_buy_binary(game.board, game.player)
    op_can_buy = can_buy_binary(game.board, game.opponent)
    tokens = tokens_binary(game.tokens)
    for noble in game.nobles:
        output.append(price_binary(noble=noble))
    for row in game.board:
        for card in row:
            output.append(price_binary(card=card))
    output.append(can_buy)
    output.append(op_can_buy)
    output.append(tokens)
    # print(output)
    return tuple(output)

# This function takes a game and returns its player's fitness
# In the future this will return a tuple of the player and opponent's fitness
def get_fitness(game):
    pass
