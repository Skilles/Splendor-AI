import os
import random
from operator import attrgetter

import pygame

pygame.init()

import util

FPS = 60

info = pygame.display.Info()
WIN_WIDTH = info.current_w
WIN_HEIGHT = info.current_h - 50
FULLSCREEN = False
SHOW_WELCOME = False

pygame.display.set_caption('Splendor')
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), depth=16)

if FULLSCREEN:
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT + 50), flags, 16)
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
# smallerfont = pygame.font.Font('font/numbers.otf', 30)
# myfont = pygame.font.Font(None, 60)
# [black, red, green, blue, white]
screen.fill((255, 255, 255))

bg = pygame.transform.scale(pygame.image.load(util.resource_path('bg.jpg')),
                            (info.current_w, info.current_h)).convert()
smallerfont = pygame.font.Font(None, 56)
pointfont = pygame.font.Font(None, 110)
smallerfont.set_italic(True)
screen.blit(bg, (0, 0))
logo = pygame.transform.scale(pygame.image.load(util.resource_path('logo.png')), (249, 100)).convert_alpha()
player_token_box = pygame.image.load(
    os.path.join('textures',
                 'token_storage.png')).convert_alpha()
token_box_rect = None
noble_images = {1: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((0, 0, 180, 180)).convert(),
                2: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((180, 0, 180, 180)).convert(),
                3: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((360, 0, 180, 180)).convert(),
                4: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((540, 0, 180, 180)).convert(),
                5: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((720, 0, 180, 180)).convert(),
                6: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((900, 0, 180, 180)).convert(),
                7: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((1080, 0, 180, 180)).convert(),
                8: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((1260, 0, 180, 180)).convert(),
                9: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((1440, 0, 180, 180)).convert(),
                10: pygame.image.load(util.resource_path('nobles.jpg')).subsurface((1620, 0, 180, 180)).convert(),
                }
card_backs = {'white': [[pygame.image.load(util.resource_path('cards.jpg')).subsurface((1380, 0, 230, 320)).convert()],
                        [pygame.image.load(util.resource_path('cards.jpg')).subsurface((1610, 0, 230, 320)).convert()],
                        [pygame.image.load(util.resource_path('cards.jpg')).subsurface((1840, 0, 230, 320)).convert()]],
              'blue': [[pygame.image.load(util.resource_path('blue_back1.jpg')).convert(),
                        pygame.image.load(util.resource_path('cards.jpg')).subsurface((690, 0, 230, 320)).convert()],
                       [pygame.image.load(util.resource_path('cards.jpg')).subsurface((920, 0, 230, 320)).convert()],
                       [pygame.image.load(util.resource_path('blue_back3.jpg')).convert(),
                        pygame.image.load(util.resource_path('cards.jpg')).subsurface((1150, 0, 230, 320)).convert()]],
              'green': [[pygame.image.load(util.resource_path('cards.jpg')).subsurface((2070, 0, 230, 320)).convert()],
                        [pygame.image.load(util.resource_path('green_back2.jpg')).convert(),
                         pygame.image.load(util.resource_path('cards.jpg')).subsurface((2300, 0, 230, 320)).convert()],
                        [pygame.image.load(util.resource_path('cards.jpg')).subsurface((2530, 0, 230, 320)).convert()]],
              'red': [[pygame.image.load(util.resource_path('cards.jpg')).subsurface((2760, 0, 230, 320)).convert()],
                      [pygame.image.load(util.resource_path('cards.jpg')).subsurface((2990, 0, 230, 320)).convert()],
                      [pygame.image.load(util.resource_path('red_back3.jpg')).convert(),
                       pygame.image.load(util.resource_path('cards.jpg')).subsurface((3220, 0, 230, 320)).convert()]],
              'black': [[pygame.image.load(util.resource_path('black_back1.jpg')).convert(),
                         pygame.image.load(util.resource_path('cards.jpg')).subsurface((0, 0, 230, 320)).convert()],
                        [pygame.image.load(util.resource_path('cards.jpg')).subsurface((230, 0, 230, 320)).convert()],
                        [pygame.image.load(util.resource_path('cards.jpg')).subsurface((460, 0, 230, 320)).convert()]]}


class Game:
    def __init__(self, genome=None, genomes=None, network=None):
        if genomes is None:
            genomes = [genome, 0]
        self.genomes = genomes
        self.network = network
        self.player = Player(self, genomes[0])
        self.opponent = Opponent(self, genomes[1])
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.decks = [[
            Card('black', 0, 1, 1, 1, 1, 0),  # white=0, blue=0, green=0, red=0, black=0
            Card('black', 0, 1, 2, 1, 1, 0),
            Card('black', 0, 2, 2, 0, 1, 0),
            Card('black', 0, 0, 0, 1, 3, 1),
            Card('black', 0, 0, 0, 2, 1, 0),
            Card('black', 0, 2, 0, 2, 0, 0),
            Card('black', 0, 0, 0, 3, 0, 0),
            Card('black', 1, 0, 4, 0, 0, 0),
            Card('blue', 0, 1, 0, 1, 1, 1),
            Card('blue', 0, 1, 0, 1, 2, 1),
            Card('blue', 0, 1, 0, 2, 2, 0),
            Card('blue', 0, 0, 1, 3, 1, 0),
            Card('blue', 0, 1, 0, 0, 0, 2),
            Card('blue', 0, 0, 0, 2, 0, 2),
            Card('blue', 0, 0, 0, 0, 0, 3),
            Card('blue', 1, 0, 0, 0, 4, 0),
            Card('white', 0, 0, 1, 1, 1, 1),
            Card('white', 0, 0, 1, 2, 1, 1),
            Card('white', 0, 0, 2, 2, 0, 1),
            Card('white', 0, 3, 1, 0, 0, 1),
            Card('white', 0, 0, 0, 0, 2, 1),
            Card('white', 0, 0, 2, 0, 0, 2),
            Card('white', 0, 0, 3, 0, 0, 0),
            Card('white', 1, 0, 0, 4, 0, 0),
            Card('green', 0, 1, 1, 0, 1, 1),
            Card('green', 0, 1, 1, 0, 1, 2),
            Card('green', 0, 0, 1, 0, 2, 2),
            Card('green', 0, 1, 3, 1, 0, 0),
            Card('green', 0, 2, 1, 0, 0, 0),
            Card('green', 0, 0, 2, 0, 2, 0),
            Card('green', 0, 0, 0, 0, 3, 0),
            Card('green', 1, 0, 0, 0, 0, 4),
            Card('red', 0, 1, 1, 1, 0, 1),
            Card('red', 0, 2, 1, 1, 0, 1),
            Card('red', 0, 2, 0, 1, 0, 2),
            Card('red', 0, 1, 0, 0, 1, 3),
            Card('red', 0, 0, 2, 1, 0, 0),
            Card('red', 0, 2, 0, 0, 2, 0),
            Card('red', 0, 3, 0, 0, 0, 0),
            Card('red', 1, 4, 0, 0, 0, 0),
        ],
            [
                Card('black', 1, 3, 2, 2, 0, 0),
                Card('black', 1, 3, 0, 3, 0, 2),
                Card('black', 2, 0, 1, 4, 2, 0),
                Card('black', 2, 0, 0, 5, 3, 0),
                Card('black', 2, 5, 0, 0, 0, 0),
                Card('black', 3, 0, 0, 0, 0, 6),
                Card('blue', 1, 0, 2, 2, 3, 0),
                Card('blue', 1, 0, 2, 3, 0, 3),
                Card('blue', 2, 5, 3, 0, 0, 0),
                Card('blue', 2, 2, 0, 0, 1, 4),
                Card('blue', 2, 0, 5, 0, 0, 0),
                Card('blue', 3, 0, 6, 0, 0, 0),
                Card('white', 1, 0, 0, 3, 2, 2),
                Card('white', 1, 2, 3, 0, 3, 0),
                Card('white', 2, 0, 0, 1, 4, 2),
                Card('white', 2, 0, 0, 0, 5, 3),
                Card('white', 2, 0, 0, 0, 5, 0),
                Card('white', 3, 6, 0, 0, 0, 0),
                Card('green', 1, 3, 0, 2, 3, 0),
                Card('green', 1, 2, 3, 0, 0, 2),
                Card('green', 2, 4, 2, 0, 0, 1),
                Card('green', 2, 0, 5, 3, 0, 0),
                Card('green', 2, 0, 0, 5, 0, 0),
                Card('green', 3, 0, 0, 6, 0, 0),
                Card('red', 1, 2, 0, 0, 2, 3),
                Card('red', 1, 0, 3, 0, 2, 3),
                Card('red', 2, 1, 4, 2, 0, 0),
                Card('red', 2, 3, 0, 0, 0, 5),
                Card('red', 2, 0, 0, 0, 0, 5),
                Card('red', 3, 0, 0, 0, 6, 0),
            ],
            [
                Card('black', 3, 3, 3, 5, 3, 0),
                Card('black', 4, 0, 0, 0, 7, 0),
                Card('black', 4, 0, 0, 3, 6, 3),
                Card('black', 5, 0, 0, 0, 7, 3),
                Card('blue', 3, 3, 0, 3, 3, 5),
                Card('blue', 4, 7, 0, 0, 0, 0),
                Card('blue', 4, 6, 3, 0, 0, 3),
                Card('blue', 5, 7, 3, 0, 0, 0),
                Card('white', 3, 0, 3, 3, 5, 3),
                Card('white', 4, 0, 0, 0, 0, 7),
                Card('white', 4, 3, 0, 0, 3, 6),
                Card('white', 5, 3, 0, 0, 0, 7),
                Card('green', 3, 5, 3, 0, 3, 3),
                Card('green', 4, 0, 7, 0, 0, 0),
                Card('green', 4, 3, 6, 3, 0, 0),
                Card('green', 5, 0, 7, 3, 0, 0),
                Card('red', 3, 3, 5, 3, 0, 3),
                Card('red', 4, 0, 0, 7, 0, 0),
                Card('red', 4, 0, 3, 6, 3, 0),
                Card('red', 5, 0, 0, 7, 3, 0),
            ]]  # 0 = green, 1 = yellow, 2 = blue
        self.nobles = []
        self.tokens = bank_tokens()
        self.timer = 0
        self.turn = self.player
        self.last_turn = False
        self.end = False
        self.setup_board()

    def run(self, events):
        global clicked
        pos = pygame.mouse.get_pos()
        if clock.get_fps() > 0:
            self.timer += 1 / clock.get_fps()
        if self.turn == self.opponent:
            self.opponent.do_action()
        if self.end:
            print(f"Winner: {self.winner}")
            return False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not clicked and self.turn == self.player:
                if event.button == 1:
                    if isinstance(hovered, Token) and \
                            len(self.player.tokens) < 10 and hovered.color != 'yellow':
                        self.player.take_token(hovered)
                        if self.player.double_take or len(self.player.taken) == 3:
                            self.end_turn()
                        break
                    elif isinstance(hovered, Card) and not self.player.has_taken() and hovered != 0 and \
                            hovered.sprite.collidepoint(pos) == 1 and self.player.can_buy(hovered):
                        self.player.buy(hovered)
                        self.end_turn()
                        break
                elif event.button == 3:
                    for row in self.board:
                        for card in row:
                            if card != 0 and card.sprite.collidepoint(pos) == 1 and len(self.player.reserved) < 3:
                                self.player.reserve(card)
                                self.end_turn()
                                return True
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
        return True

    def setup_board(self):
        global noble_pool
        self.init_cards()
        for row in range(0, 3):
            for _ in range(0, 4):
                self.draw_card(row)
        for _ in range(0, 3):
            noble = random.choice(noble_pool)
            noble_pool.remove(noble)
            self.nobles.append(noble)
        for noble in self.nobles:
            util.stamp_noble(noble)

    def draw_card(self, row):
        deck = self.decks[2 - row]
        if len(deck) > 0:
            row = self.board[row]
            card = random.choice(deck)
            deck.remove(card)
            for i, space in enumerate(row):
                if space == 0:
                    row[i] = card
                    break
            return card

    def end_turn(self):
        self.check_win()
        self.check_nobles()
        self.turn.double_take = False
        self.turn.taken.clear()
        if self.turn == self.player:
            self.turn = self.opponent
        else:
            self.turn = self.player

    def check_nobles(self):
        for noble in self.nobles:
            if self.turn.can_claim(noble) and not self.turn.claimed:
                self.give_noble(noble, self.turn)
                break

    def check_win(self):
        if self.player.points >= 15:
            self.last_turn = True
        if self.opponent.points >= 15:
            self.winner = self.opponent
            return True
        if self.last_turn:
            self.end = True
            if self.player.points == self.opponent.points:
                if len(self.opponent.cards) == len(self.player.cards):
                    self.winner = 'Tied'
                else:
                    # Gets player with most amount of cards
                    self.winner = max([self.player, self.opponent], key=lambda player: len(player.cards))
            else:
                self.winner = max([self.player, self.opponent], key=attrgetter('points'))
            return True

    def give_noble(self, noble, player):
        self.nobles.remove(noble)
        player.nobles.append(noble)
        player.claimed = True

    def init_cards(self):
        for i, deck in enumerate(self.decks):
            for card in deck:
                card.img = pygame.transform.scale(random.choice(card_backs[card.color][i]), (226, 315))
                util.stamp_card(card)
                card.level = get_level(card, self)


class Player:
    def __init__(self, game, genome=None):
        self.genome = genome
        self.points = 0
        self.tokens = []
        self.cards = []
        self.nobles = []
        self.reserved = None
        self.game = game
        self.claimed = False
        self.taken = []
        self.reserved = []
        self.double_take = False

    def take_token(self, token=None, color=None):
        if not token:
            token = Token(color, self)
        if self.has_taken(token):
            if len(self.taken) > 1 or len(util.get_colors(self.game.tokens, token.color)) < 4:
                return False
            else:
                self.double_take = True
        self.game.tokens.remove(token)
        self.tokens.append(token)
        self.taken.append(token)
        util.highlight_cards(self.game.board, self)
        return True

    def buy(self, card):
        yellows = len(util.get_colors(self.tokens, 'yellow'))
        for x in range(0, 5):
            cost = card.price[x] - len(util.get_colors(self.cards, util.index_to_color(x)))
            if cost != 0:
                for _ in range(0, cost):
                    try:
                        token = util.get_color(self.tokens, util.index_to_color(x))
                    except Exception:
                        if yellows != 0:
                            token = util.get_color(self.tokens, 'yellow')
                        else:
                            raise AssertionError("Not enough yellows!")
                    token.holder = None
                    self.tokens.remove(token)
                    self.game.tokens.append(token)
        util.highlight_cards(self.game.board, self)

        row = 2 - card.level
        if self.game.board[row].__contains__(card):
            index = self.game.board[row].index(card)
            self.game.board[row][index] = self.game.draw_card(row)
            if not self.game.board[row][index]:
                self.game.board[row][index] = 0
                print('All cards in this deck are drawn!')
        else:
            self.reserved.remove(card)
        card.holder = self
        self.cards.append(card)
        self.points += card.points

    def reserve(self, card):
        row = 2 - card.level
        index = self.game.board[row].index(card)
        card.holder = self
        self.reserved.append(card)
        self.game.board[row][index] = self.game.draw_card(row)
        self.take_token(color='yellow')

    def can_buy(self, card):
        yellows = len(util.get_colors(self.tokens, 'yellow'))
        for i in range(0, 5):
            cost = card.price[i]
            pp = len(util.get_colors(self.tokens, util.index_to_color(i))) + len(
                util.get_colors(self.cards, util.index_to_color(i)))
            if cost > pp:
                if cost <= pp + yellows:
                    yellows = pp + yellows - cost
                    continue
                return False
        return True

    def can_claim(self, noble):
        for i in range(0, 5):
            if noble.price[i] > len(
                    util.get_colors(self.cards, util.index_to_color(i))):
                return False
        return True

    def has_taken(self, token=None):
        if token:
            return self.taken.__contains__(token)
        return len(self.taken) != 0

    def __repr__(self):
        return 'Player'


class Opponent(Player):
    def do_action(self):
        if not self.has_taken():
            for row in self.game.board:
                for card in row:
                    if card != 0 and self.can_buy(card):
                        self.buy(card)
                        self.game.end_turn()
                        return
        count = 0
        while count < 3:
            color = util.index_to_color(random.randrange(0, 5))
            if not self.taken.__contains__(Token(color)):
                self.take_token(color=color)
                count += 1
        self.game.end_turn()

    def __repr__(self):
        return 'Opponent'


class Card:
    def __init__(self, color, points, white=0, blue=0, green=0, red=0, black=0, holder=None):
        self.price = [black, red, green, blue, white]
        self.points = points
        self.color = color
        self.sprite = None
        self.img = None
        self.highlight = False
        self.holder = holder
        self.level = 0

    def __repr__(self):
        return f'{self.level} | {self.color} | {self.price}'


class Token:
    def __init__(self, color, holder=None):
        self.color = color
        self.holder = holder
        self.img = get_token_img(color)
        self.sprite = None

    def __repr__(self):
        return f'{self.color.capitalize()} Token | {self.holder}'

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.color == other.color


class Noble:
    def __init__(self, id, points, white=0, blue=0, green=0, red=0, black=0):
        self.id = id
        self.price = [black, red, green, blue, white]
        self.points = points
        self.sprite = None
        self.img = noble_images[id]

    def __repr__(self):
        return f'{self.id} | {self.points} | {self.price}'


def bank_tokens():
    tokens = []
    for _ in range(0, 7):
        tokens.append(Token('red', None))
        tokens.append(Token('blue', None))
        tokens.append(Token('green', None))
        tokens.append(Token('white', None))
        tokens.append(Token('black', None))
    for _ in range(0, 5):
        tokens.append(Token('yellow', None))
    return tokens


noble_pool = [
    Noble(1, 3, 0, 0, 0, 4, 4),
    Noble(2, 3, 0, 0, 3, 3, 3),
    Noble(3, 3, 0, 4, 4, 0, 0),
    Noble(4, 3, 4, 4, 0, 0, 0),
    Noble(5, 3, 3, 3, 0, 0, 3),
    Noble(6, 3, 0, 0, 4, 4, 0),
    Noble(7, 3, 0, 3, 3, 3, 0),
    Noble(8, 3, 4, 0, 0, 0, 4),
    Noble(9, 3, 3, 3, 3, 0, 0),
    Noble(10, 3, 3, 0, 0, 3, 3),
]


def get_level(card, game):
    for i, deck in enumerate(game.decks):
        if deck.__contains__(card):
            return i


def draw_nobles(nobles):
    y_offset = noble_images[1].get_height() + 20
    x_initial = 250
    y_initial = 300
    x = x_initial

    for i, noble in enumerate(nobles):
        y = y_initial + y_offset * i
        noble.sprite = screen.blit(noble.img, (x, y))


def draw_bank(tokens):
    x_offset = 6
    y_offset = 10
    x_initial = 2000
    y_initial = 150
    y_spacing = green_token.get_height() * 1.5 - 15
    y_bank = 150
    y_bank_offset = green_token.get_height() + 50
    x_bank = 1950
    for i in range(0, 6):
        x = x_initial
        y = y_initial + y_spacing * i
        color = util.index_to_color(i)
        gems = util.get_colors(tokens, color)
        for gem in gems:
            if gem.color == 'yellow':
                y -= y_offset // 2
            gem.sprite = screen.blit(gem.img, (x, y))
            x += x_offset
            y -= y_offset
        # Print bank numbers
        y = y_bank
        amount = len([token for token in tokens if token.color == color])
        if amount > 0:
            label = myfont.render(str(amount), True,
                                  (255, 255, 255))
            screen.blit(label, (x_bank, y))
            y_bank += y_bank_offset


def draw_reserved(reserved):
    x_offset = card_backs['white'][0][0].get_width() // 2 + 10
    extra_offset = 0
    for i, card in enumerate(reserved):
        x = token_box_rect.x + token_box_rect.width - 50 + x_offset * i + extra_offset
        y = token_box_rect.y - 10
        if hovered == card:
            resized_img = pygame.transform.scale(card.img,
                                                 (int(card.img.get_width() // 1.5), int(card.img.get_height() // 1.5)))
            y -= 50
            extra_offset = 30
        else:
            resized_img = pygame.transform.scale(card.img, (card.img.get_width() // 2, card.img.get_height() // 2))
        card.sprite = screen.blit(resized_img, (x, y))


def draw_tokens(tokens, opponent=False):
    x_offset = 0
    y_offset = 5
    x_initial = token_box_rect.x + token_box_rect.width - 295
    y_initial = 1295
    x_spacing = green_token.get_width() + 17

    x_initial_label = token_box_rect.x + token_box_rect.width - 275
    y_offset_label = 57
    x_spacing_label = green_token.get_width() + 17

    if opponent:
        x_offset = 6
        y_offset = 10
        y_initial = 70
    else:
        label = myfont.render(f'{len(tokens)} / 10', True, (255, 255, 255))
        screen.blit(label, (token_box_rect.x - 40, token_box_rect.y + 30))
    for i in range(0, 6):
        x = x_initial - x_spacing * i
        y = y_initial
        color = util.index_to_color(i)
        for gem in [gem for gem in tokens if gem.color == color]:
            gem.sprite = screen.blit(
                pygame.transform.scale(gem.img, (int(gem.img.get_width() / 2), int(gem.img.get_height() / 2))),
                (x, y))
            x += x_offset
            y -= y_offset
        if not opponent:
            x = x_initial_label - x_spacing_label * i
            color = util.index_to_color(i)
            y = get_top(tokens, color)
            if y:
                y = y.sprite.y - y_offset_label
                label = myfont.render(str(len([token for token in tokens if token.color == color])), True,
                                      (255, 255, 255))
                screen.blit(label, (x, y))


def draw_board(game):
    x_initial = 325
    y_initial = 150

    green_length = len(game.decks[0])
    yellow_length = len(game.decks[1])
    blue_length = len(game.decks[2])
    if green_length >= 5:
        green_length //= 3
    if yellow_length >= 5:
        yellow_length //= 3
    if blue_length >= 5:
        blue_length //= 3
    x_offset = green_deck.get_width() + 25
    y_offset = green_deck.get_height() + 10
    for i, row in enumerate(game.board):
        y = y_initial + y_offset * i
        x = x_initial + green_deck.get_width() + x_offset
        for card in row:
            if card != 0:
                card.sprite = screen.blit(card.img, (x, y))
            x += x_offset
        x = x_initial + 200
        if i == 2:
            length = green_length
            deck = green_deck
        elif i == 1:
            length = yellow_length
            deck = yellow_deck
        elif i == 0:
            length = blue_length
            deck = blue_deck
        for _ in range(0, length):
            screen.blit(deck, (x, y))
            x += 3
            y -= 1


def draw_cards(game):
    draw_board(game)
    x = token_box_rect.x + 265
    y = token_box_rect.y + 30
    x_offset = green_token.get_width() + 17
    # Reverse for some reason TODO: !!
    for i in range(4, -1, -1):
        color = pygame.Color(util.index_to_rgb(i))
        color.update(color.r, color.g, color.b, 120)
        pygame.draw.rect(screen, color, (x + 3, y + 3, 66, 106), border_radius=10)
        if i != 0 and i != 3:
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 72, 112), 3, border_radius=10)
            label = myfont.render(str(len(util.get_colors(game.player.cards, util.index_to_color(i)))), True,
                                  (0, 0, 0))
        else:  # black
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 72, 112), 3, border_radius=10)
            label = myfont.render(str(len(util.get_colors(game.player.cards, util.index_to_color(i)))), True,
                                  (255, 255, 255))
        screen.blit(label, (x + 10, y + 40))
        x += x_offset


def draw_text(game):
    label = smallFont.render(f'Time: {int(game.timer)}', True, (255, 255, 255))
    screen.blit(label, (10, 10))
    label = smallFont.render(f'You: {game.player.points}', True, (255, 255, 255))
    screen.blit(label, (screen.get_width() - label.get_width() - 10, 10))
    label = smallFont.render(f'Opponent: {game.player.points}', True, (255, 255, 255))
    screen.blit(label, (screen.get_width() - label.get_width() - 10, 40))
    label = smallFont.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
    screen.blit(label, (10, 40))
    screen.blit(logo, ((screen.get_width() - logo.get_width()) / 2, 30))


def draw_clicked():
    pos = pygame.mouse.get_pos()
    if clicked:
        clicked.sprite = screen.blit(clicked.img,
                                     (pos[0] - clicked.img.get_width() / 2,
                                      pos[1] - clicked.img.get_height() / 2))


hovered = None


def check_collision(game):
    global hovered
    pos = pygame.mouse.get_pos()
    hovered = None
    for row in game.board:
        for card in row:
            if card != 0 and card.sprite.collidepoint(pos) == 1:
                pygame.draw.rect(screen, util.red,
                                 (card.sprite.x, card.sprite.y, card.sprite.width, card.sprite.height), 3,
                                 border_radius=10)
                hovered = card
                break
            elif card != 0 and card.highlight:
                pygame.draw.rect(screen, util.blue,
                                 (card.sprite.x, card.sprite.y, card.sprite.width, card.sprite.height), 3,
                                 border_radius=10)
    for card in game.player.reserved:
        if card.sprite.collidepoint(pos) == 1:
            pygame.draw.rect(screen, util.red,
                             (card.sprite.x, card.sprite.y, card.sprite.width, card.sprite.height), 3,
                             border_radius=5)
            hovered = card
            break
        elif card.highlight:
            pygame.draw.rect(screen, util.blue,
                             (card.sprite.x, card.sprite.y, card.sprite.width, card.sprite.height), 3,
                             border_radius=5)
    for token in game.tokens:
        if token.sprite.collidepoint(pos) == 1:
            hovered = token
            break


def draw_game(game):
    global token_box_rect
    draw_text(game)
    draw_bank(game.tokens)
    token_box_rect = screen.blit(player_token_box, (WIN_WIDTH / 2 - player_token_box.get_width() / 2, WIN_HEIGHT - 178))
    draw_cards(game)
    draw_tokens(game.player.tokens)
    draw_tokens(game.opponent.tokens, True)
    # draw_token_numbers(game.player.tokens, game.tokens)
    draw_nobles(game.nobles)
    draw_reserved(game.player.reserved)
    check_collision(game)
    # draw_clicked()


clicked = None
sprites_to_update = []


def update_screen():
    global sprites_to_update
    # pygame.display.update(sprites_to_update)
    pygame.display.update()
    pygame.display.flip()


def show_welcome():
    load = False
    while not load:
        events = pygame.event.get()
        # pygame.display.update()
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                load = True
                break
            elif e.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
        clock.tick(FPS)
        screen.blit(bg, (0, 0))
        # label = myfont.render('Welcome to Splendor!', True, (255, 255, 255))
        # screen.blit(label, ((screen.get_width() - label.get_width()) // 2, screen.get_height() // 3))\\
        # resized_logo = pygame.transform.scale(logo, (logo.get_width() * 2, logo.get_height() * 2))
        resized_logo = pygame.transform.scale2x(logo)
        screen.blit(resized_logo, ((screen.get_width() - resized_logo.get_width()) // 2, screen.get_height() // 3))
        # label = smallerfont.render('Press space to continue', True, (255, 191, 0))
        label = util.with_outline('Press space to continue', smallerfont, (255, 191, 0))
        screen.blit(label, ((screen.get_width() - label.get_width()) // 2, screen.get_height() // 3 + 200))
        update_screen()


def main(genome=None, network=None):
    if SHOW_WELCOME:
        show_welcome()
    run = True
    game = Game(genome)
    while run:
        events = pygame.event.get()
        # pygame.display.update()
        clock.tick(FPS)
        screen.blit(bg, (0, 0))
        if not game.run(events):
            run = False
            return game
        draw_game(game)
        update_screen()
        # pygame.display.flip()


def get_token_img(color):
    if color == 'red':
        return red_token
    elif color == 'green':
        return green_token
    elif color == 'blue':
        return blue_token
    elif color == 'yellow':
        return yellow_token
    elif color == 'white':
        return white_token
    elif color == 'black':
        return black_token


def get_top(tokens, color):
    tokens = [token for token in tokens if token.color == color]
    top = 0
    top_token = None
    for token in tokens:
        if WIN_HEIGHT - token.sprite.y > top:
            top = WIN_HEIGHT - token.sprite.y
            top_token = token
    return top_token


info = pygame.display.Info()
myfont = pygame.font.Font('font/numbers.otf', 60)
smallFont = pygame.font.SysFont('monospace', 30)
clock = pygame.time.Clock()
red_token = pygame.image.load(util.resource_path('red_token.png')).convert_alpha()
yellow_token = pygame.image.load(util.resource_path('yellow_token.png')).convert_alpha()
green_token = pygame.image.load(util.resource_path('green_token.png')).convert_alpha()
black_token = pygame.image.load(util.resource_path('black_token.png')).convert_alpha()
white_token = pygame.image.load(util.resource_path('white_token.png')).convert_alpha()
blue_token = pygame.image.load(util.resource_path('blue_token.png')).convert_alpha()
green_deck = pygame.image.load(util.resource_path('deck.png')).subsurface((0, 0, 226, 315)).convert_alpha()
yellow_deck = pygame.image.load(util.resource_path('deck.png')).subsurface((226, 0, 226, 315)).convert_alpha()
blue_deck = pygame.image.load(util.resource_path('deck.png')).subsurface((456, 0, 226, 315)).convert_alpha()
gem_imgs = {'white': pygame.image.load(util.resource_path('white_gem.png')).convert_alpha(),
            'blue': pygame.image.load(util.resource_path('blue_gem.png')).convert_alpha(),
            'green': pygame.image.load(util.resource_path('green_gem.png')).convert_alpha(),
            'red': pygame.image.load(util.resource_path('red_gem.png')).convert_alpha(),
            'black': pygame.image.load(util.resource_path('black_gem.png')).convert_alpha()}
