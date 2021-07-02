import os
import random

import pygame

pygame.init()

import util

FPS = 60

info = pygame.display.Info()
WIN_WIDTH = info.current_w
WIN_HEIGHT = info.current_h - 50
FULLSCREEN = False

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
card_backs = {'white': [[pygame.image.load(util.resource_path('blue_back1.jpg')).convert()],
                        [pygame.image.load(util.resource_path('blue_back1.jpg')).convert()],
                        [pygame.image.load(util.resource_path('blue_back1.jpg')).convert()]],
              'blue': [[pygame.image.load(util.resource_path('blue_back1.jpg')).convert()],
                       [pygame.image.load(util.resource_path('blue_back1.jpg')).convert()],
                       [pygame.image.load(util.resource_path('blue_back3.jpg')).convert()]],
              'green': [[pygame.image.load(util.resource_path('blue_back1.jpg')).convert()],
                        [pygame.image.load(util.resource_path('green_back2.jpg')).convert()],
                        [pygame.image.load(util.resource_path('blue_back1.jpg')).convert()]],
              'red': [[pygame.image.load(util.resource_path('blue_back1.jpg')).convert()],
                      [pygame.image.load(util.resource_path('blue_back1.jpg')).convert()],
                      [pygame.image.load(util.resource_path('red_back3.jpg')).convert()]],
              'black': [[pygame.image.load(util.resource_path('black_back1.jpg')).convert()],
                        [pygame.image.load(util.resource_path('blue_back1.jpg')).convert()],
                        [pygame.image.load(util.resource_path('blue_back1.jpg')).convert()]]}


class Game:
    def __init__(self):
        self.player = Player(self)
        self.opponent = Opponent(self)
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
        self.setup_board()

    def run(self, events):
        global clicked
        pos = pygame.mouse.get_pos()
        if clock.get_fps() > 0:
            self.timer += 1 / clock.get_fps()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not clicked and self.turn == self.player:
                if event.button == 1:
                    for token in self.tokens:
                        if token.sprite.collidepoint(pos) == 1 and \
                                len(self.player.tokens) < 10 and token.color != 'yellow':
                            # self.tokens.remove(token)
                            # clicked = token
                            self.player.take_token(token)
                            if self.player.double_take or len(self.player.taken) == 3:
                                self.end_turn()
                            break
                    for row in self.board:
                        for card in row:
                            if card != 0:
                                if card.sprite.collidepoint(pos) == 1 and self.player.can_buy(card):
                                    self.player.buy(card)
                                    self.end_turn()
                                    break
                elif event.button == 3:
                    for row in self.board:
                        for card in row:
                            if card != 0:
                                if card.sprite.collidepoint(pos) == 1:
                                    self.player.reserve(card)
                                    self.end_turn()
                                    break

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
        # elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked:
        #     if token_box_rect.collidepoint(pos) == 1 and len(self.player.tokens) < 10:
        #         self.player.tokens.append(clicked)
        #     else:
        #         clicked.holder = None
        #         self.tokens.append(clicked)
        #     clicked = None

    def setup_board(self):
        global noble_pool
        self.init_cards()
        for row in range(0, 3):
            for column in range(0, 4):
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
        self.check_nobles()
        self.turn.double_take = False
        self.turn.taken.clear()
        if self.turn == self.player:
            self.turn = self.opponent
        else:
            self.turn = self.player

    def check_nobles(self):
        for noble in self.nobles:
            player = self.player
            for _ in range(0, 2):
                if player.can_claim(noble) and self.turn == player and not player.claimed:
                    self.give_noble(noble, self.player)
                player = self.opponent

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
        if self.taken.__contains__(token):
            if len(self.taken) > 1:
                return False
            else:
                self.double_take = True
        self.game.tokens.remove(token)
        self.tokens.append(token)
        self.taken.append(token)

    def buy(self, card):
        for x in range(0, 5):
            cost = card.price[x] - len(util.get_colors(self.cards, util.index_to_color(x)))
            for i in range(0, cost):
                token = util.get_color(self.tokens, util.index_to_color(x))
                token.holder = None
                self.tokens.remove(token)
                self.game.tokens.append(token)
        row = 2 - card.level
        index = self.game.board[row].index(card)
        card.holder = self
        self.cards.append(card)
        self.points += card.points
        self.game.board[row][index] = self.game.draw_card(row)
        if not self.game.board[row][index]:
            self.game.board[row][index] = 0
            print('All cards in this deck are drawn!')

    def reserve(self, card):
        row = 2 - card.level
        index = self.game.board[row].index(card)
        card.holder = self
        self.reserved.append(card)
        self.game.board[row][index] = self.game.draw_card(row)

    def can_buy(self, card):
        for i in range(0, 5):
            if card.price[i] > len(util.get_colors(self.tokens, util.index_to_color(i))) + len(
                    util.get_colors(self.cards, util.index_to_color(i))):
                return False
        return True

    def can_claim(self, noble):
        for i in range(0, 5):
            if noble.price[i] > len(
                    util.get_colors(self.cards, util.index_to_color(i))):
                return False
        return True


class Opponent(Player):
    pass


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
        return f'{self.color.capitalize()} Token'

    def __eq__(self, other):
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
    for i in range(0, 7):
        tokens.append(Token('red', None))
        tokens.append(Token('blue', None))
        tokens.append(Token('green', None))
        tokens.append(Token('white', None))
        tokens.append(Token('black', None))
    for i in range(0, 5):
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
    x = x_initial
    for i in range(0, 6):
        x = x_initial
        y = y_initial + y_spacing * i
        gems = util.get_colors(tokens, util.index_to_color(i))
        for gem in gems:
            if gem.color == 'yellow':
                y -= y_offset // 2
            gem.sprite = screen.blit(gem.img, (x, y))
            x += x_offset
            y -= y_offset


def draw_reserved(reserved):
    if len(reserved) > 0:
        card = reserved[0]
        print(card)
        x_initial = token_box_rect.x + token_box_rect.width - 50
        y_initial = token_box_rect.y - 10
        resized_img = pygame.transform.scale(card.img, (card.img.get_width() // 2, card.img.get_height() // 2))
        card.sprite = screen.blit(resized_img, (x_initial, y_initial))


def draw_tokens(tokens, opponent=False):
    x_offset = 0
    y_offset = 5
    x_initial = token_box_rect.x + 340
    y_initial = 1295
    x_spacing = green_token.get_width() + 17
    x = x_initial
    y = y_initial
    if opponent:
        x_offset = 6
        y_offset = 10
        y_initial = 100
    for i in range(0, 6):
        x = x_initial + x_spacing * i
        if i == 0:
            for gem in [gem for gem in tokens if gem.color == 'white']:
                gem.sprite = screen.blit(
                    pygame.transform.scale(gem.img, (int(gem.img.get_width() / 2), int(gem.img.get_height() / 2))),
                    (x, y))
                x += x_offset
                y -= y_offset
            y = y_initial
        elif i == 1:
            for gem in [gem for gem in tokens if gem.color == 'blue']:
                gem.sprite = screen.blit(
                    pygame.transform.scale(gem.img, (int(gem.img.get_width() / 2), int(gem.img.get_height() / 2))),
                    (x, y))
                x += x_offset
                y -= y_offset
            y = y_initial
        elif i == 2:
            for gem in [gem for gem in tokens if gem.color == 'green']:
                gem.sprite = screen.blit(
                    pygame.transform.scale(gem.img, (int(gem.img.get_width() / 2), int(gem.img.get_height() / 2))),
                    (x, y))
                x += x_offset
                y -= y_offset
            y = y_initial
        elif i == 3:
            for gem in [gem for gem in tokens if gem.color == 'red']:
                gem.sprite = screen.blit(
                    pygame.transform.scale(gem.img, (int(gem.img.get_width() / 2), int(gem.img.get_height() / 2))),
                    (x, y))
                x += x_offset
                y -= y_offset
            y = y_initial
        elif i == 4:
            for gem in [gem for gem in tokens if gem.color == 'black']:
                gem.sprite = screen.blit(
                    pygame.transform.scale(gem.img, (int(gem.img.get_width() / 2), int(gem.img.get_height() / 2))),
                    (x, y))
                x += x_offset
                y -= y_offset
            y = y_initial
        elif i == 5:
            for gem in [gem for gem in tokens if gem.color == 'yellow']:
                gem.sprite = screen.blit(
                    pygame.transform.scale(gem.img, (int(gem.img.get_width() / 2), int(gem.img.get_height() / 2))),
                    (x, y))
                x += x_offset
                y -= y_offset


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
                if game.player.can_buy(card):
                    card.highlight = True
                else:
                    card.highlight = False
            x += x_offset
        x = x_initial + 200
        if i == 2:
            for z in range(0, green_length):
                screen.blit(green_deck, (x, y))
                x += 2
        elif i == 1:
            for z in range(0, yellow_length):
                screen.blit(yellow_deck, (x, y))
                x += 2
        elif i == 0:
            for z in range(0, blue_length):
                screen.blit(blue_deck, (x, y))
                x += 2


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


# TODO: merge with draw_tokens & draw_bank
def draw_token_numbers(tokens, bank):
    label = myfont.render(f'{len(tokens)} / 10', True, (255, 255, 255))
    screen.blit(label, (token_box_rect.x - 40, token_box_rect.y + 30))

    x_initial = token_box_rect.x + 360
    y_offset = 57
    x_spacing = green_token.get_width() + 17
    y_bank = 280
    y_bank_offset = green_token.get_height() + 50
    x_bank = 1970
    for i in range(0, 5):
        x = x_initial + x_spacing * i
        if i == 0:
            y = get_top(tokens, 'green')
            if y:
                y = y.sprite.y - y_offset
                label = myfont.render(str(len([token for token in tokens if token.color == 'green'])), True,
                                      (255, 255, 255))
                screen.blit(label, (x, y))
            # Print bank numbers
            y = y_bank
            amount = len([token for token in bank if token.color == 'green'])
            if amount > 0:
                label = myfont.render(str(amount), True,
                                      (255, 255, 255))
                screen.blit(label, (x_bank, y))
        elif i == 1:
            y = get_top(tokens, 'white')
            if y:
                y = y.sprite.y - y_offset
                label = myfont.render(str(len([token for token in tokens if token.color == 'white'])), True,
                                      (255, 255, 255))
                screen.blit(label, (x, y))
            y = y_bank + y_bank_offset * i
            amount = len([token for token in bank if token.color == 'white'])
            if amount > 0:
                label = myfont.render(str(amount), True,
                                      (255, 255, 255))
                screen.blit(label, (x_bank, y))
        elif i == 2:
            y = get_top(tokens, 'blue')
            if y:
                y = y.sprite.y - y_offset
                label = myfont.render(str(len([token for token in tokens if token.color == 'blue'])), True,
                                      (255, 255, 255))
                screen.blit(label, (x, y))
            y = y_bank + y_bank_offset * i
            amount = len([token for token in bank if token.color == 'blue'])
            if amount > 0:
                label = myfont.render(str(amount), True,
                                      (255, 255, 255))
                screen.blit(label, (x_bank, y))
        elif i == 3:
            y = get_top(tokens, 'black')
            if y:
                y = y.sprite.y - y_offset
                label = myfont.render(str(len([token for token in tokens if token.color == 'black'])), True,
                                      (255, 255, 255))
                screen.blit(label, (x, y))
            y = y_bank + y_bank_offset * i
            amount = len([token for token in bank if token.color == 'black'])
            if amount > 0:
                label = myfont.render(str(amount), True,
                                      (255, 255, 255))
                screen.blit(label, (x_bank, y))
        elif i == 4:
            y = get_top(tokens, 'red')
            if y:
                y = y.sprite.y - y_offset
                label = myfont.render(str(len([token for token in tokens if token.color == 'red'])), True,
                                      (255, 255, 255))
                screen.blit(label, (x, y))
            y = y_bank + y_bank_offset * i
            amount = len([token for token in bank if token.color == 'red'])
            if amount > 0:
                label = myfont.render(str(amount), True,
                                      (255, 255, 255))
                screen.blit(label, (x_bank, y))


def draw_text(game):
    label = smallFont.render(f'Time: {int(game.timer)}', True, (255, 255, 255))
    screen.blit(label, (10, 10))
    label = smallFont.render(f'Points: {game.player.points}', True, (255, 255, 255))
    screen.blit(label, (screen.get_width() - label.get_width() - 10, 10))
    label = smallFont.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
    screen.blit(label, (10, 40))
    screen.blit(logo, ((screen.get_width() - logo.get_width()) / 2, 30))


def draw_clicked():
    pos = pygame.mouse.get_pos()
    if clicked:
        clicked.sprite = screen.blit(clicked.img,
                                     (pos[0] - clicked.img.get_width() / 2,
                                      pos[1] - clicked.img.get_height() / 2))


# TODO: save hovered and check collision with that
def draw_highlights(game):
    pos = pygame.mouse.get_pos()
    for row in game.board:
        for card in row:
            if card != 0 and card.sprite.collidepoint(pos) == 1:
                pygame.draw.rect(screen, util.red,
                                 (card.sprite.x, card.sprite.y, card.sprite.width, card.sprite.height), 3,
                                 border_radius=10)
            elif card != 0 and card.highlight:
                pygame.draw.rect(screen, util.blue,
                                 (card.sprite.x, card.sprite.y, card.sprite.width, card.sprite.height), 3,
                                 border_radius=10)
    for card in game.player.reserved:
        if card.sprite.collidepoint(pos) == 1:
            pygame.draw.rect(screen, util.red,
                             (card.sprite.x, card.sprite.y, card.sprite.width, card.sprite.height), 3,
                             border_radius=5)
        elif card.highlight:
            pygame.draw.rect(screen, util.blue,
                             (card.sprite.x, card.sprite.y, card.sprite.width, card.sprite.height), 3,
                             border_radius=5)


def draw_game(game):
    global token_box_rect
    draw_text(game)
    draw_bank(game.tokens)
    token_box_rect = screen.blit(player_token_box, (WIN_WIDTH / 2 - player_token_box.get_width() / 2, WIN_HEIGHT - 178))
    draw_cards(game)
    draw_tokens(game.player.tokens)
    draw_tokens(game.opponent.tokens, True)
    draw_token_numbers(game.player.tokens, game.tokens)
    draw_nobles(game.nobles)
    draw_reserved(game.player.reserved)
    draw_highlights(game)
    draw_clicked()


clicked = None
sprites_to_update = []


def update_screen():
    global sprites_to_update
    # pygame.display.update(sprites_to_update)
    pygame.display.update()
    pygame.display.flip()


def main(config=None, genome=None):
    games = [Game()]
    pygame.display.update()
    while len(games) > 0:
        events = pygame.event.get()
        # pygame.display.update()
        clock.tick(FPS)
        screen.blit(bg, (0, 0))
        games[0].run(events)
        draw_game(games[0])
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
