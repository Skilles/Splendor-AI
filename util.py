import pygame

import game

import os

red = (232, 56, 47)
blue = (57, 181, 246)
green = (49, 170, 78)
black = (74, 70, 70)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pylint: disable=no-member
    except Exception:
        base_path = os.path.abspath("textures")

    return os.path.join(base_path, relative_path)


def get_color(tokens, color):
    for token in tokens:
        if token.color == color:
            return token


def index_to_color(index):  # white=0, blue=0, green=0, red=0, black=0
    if index == 0:
        return 'black'
    elif index == 1:
        return 'red'
    elif index == 2:
        return 'green'
    elif index == 3:
        return 'blue'
    elif index == 4:
        return 'white'
    elif index == 5:
        return 'yellow'


def index_to_rgb(index):  # white=0, blue=0, green=0, red=0, black=0
    if index == 0:
        return black
    elif index == 1:
        return red
    elif index == 2:
        return green
    elif index == 3:
        return blue
    elif index == 4:
        return 255, 255, 255


# For cards/tokens
def get_colors(list, color):
    return [element for element in list if element.color == color]


def set_rounded(card):
    size = card.img.get_size()
    new_img = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(new_img, (255, 255, 255, 255), (0, 0, *size), border_radius=10)
    new_img.blit(card.img, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    card.img = new_img


_circle_cache = {}


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def with_outline(text, font, gfcolor=pygame.Color('white'), ocolor=(0, 0, 0), opx=1):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


def stamp_noble(noble):
    initial_y = noble.img.get_height() - 40

    y_offset = 58
    radius = 20
    initial_x = 25
    # Searches through prices, finds non-zero ones, and stacks them on top of each other
    overlay = pygame.Surface((noble.img.get_width() // 3.5, noble.img.get_height()))
    overlay.set_alpha(100)
    overlay.fill((255, 255, 255))
    noble.img.blit(overlay, (0, 0))
    count = 0
    for i, price in enumerate(noble.price):
        if price != 0:
            y = initial_y - y_offset * count
            count += 1
            color = index_to_rgb(i)
            pygame.draw.rect(noble.img, color,
                             (initial_x - 20, y - 20, noble.img.get_width() // 5, noble.img.get_height() // 5 + 18),
                             border_radius=4)
            if i == 4:
                pygame.draw.rect(noble.img, black,
                                 (initial_x - 20, y - 20, noble.img.get_width() // 5, noble.img.get_height() // 5 + 18),
                                 1, border_radius=4)
                label = game.smallerfont.render(str(price), True, (255, 255, 255))
            else:  # black
                pygame.draw.rect(noble.img, (255, 255, 255),
                                 (initial_x - 20, y - 20, noble.img.get_width() // 5, noble.img.get_height() // 5 + 18),
                                 1, border_radius=4)
                label = game.smallerfont.render(str(price), True, (0, 0, 0))

            # text
            noble.img.blit(with_outline(str(price), game.smallerfont),
                           (initial_x - label.get_width() // 2 - 1, y - label.get_height() // 2 + 8))
            y -= y_offset

    # label = pointfont.render(str(card.points), True, (255, 255, 230))
    noble.img.blit(with_outline(str(noble.points), game.pointfont),
                   (noble.img.get_width() - label.get_width() - 15, noble.img.get_height() - label.get_height() - 30))
    # card.img.blit(label, (initial_x - label.get_width() // 2, y - radius // 2 - 4))
    set_rounded(noble)


def stamp_card(card):
    # img = card.img.copy()
    y = card.img.get_height() - 25
    y_offset = 45
    radius = 20
    initial_x = 25
    # Searches through prices, finds non-zero ones, and stacks them on top of each other
    for i, price in enumerate(card.price):
        # y = initial_y + y_offset * (len([price for price in tmp_price if price != 0]) - i)
        color = index_to_rgb(i)
        if price != 0:
            pygame.draw.circle(card.img, color, (initial_x, y), radius)
            # border
            pygame.draw.circle(card.img, (255, 255, 255), (initial_x, y), radius, 1)
            # pygame.draw.rect(card.img, (255, 255, 255, 50),
            #                  (0, 0, card.img.get_width(), card.img.get_height() // 4.5))
            # text
            label = game.smallerfont.render(str(price), True, (255, 255, 255))
            card.img.blit(with_outline(str(price), game.smallerfont),
                          (initial_x - label.get_width() // 2 + 1, y - label.get_height() // 2 + 1))
            y -= y_offset
    overlay = pygame.Surface((card.img.get_width(), card.img.get_height() // 4.5))
    overlay.set_alpha(100)
    overlay.fill((255, 255, 255))
    card.img.blit(overlay, (0, 0))
    gem_img = game.gem_imgs[card.color]
    gem_img = pygame.transform.scale(gem_img, (int(gem_img.get_width() / 1.5), int(gem_img.get_height() / 1.5)))
    card.img.blit(gem_img, (card.img.get_width() - gem_img.get_width() - 7, 5))
    if card.points != 0:
        # label = pointfont.render(str(card.points), True, (255, 255, 230))
        card.img.blit(with_outline(str(card.points), game.pointfont), (10, 0))
        # card.img.blit(label, (initial_x - label.get_width() // 2, y - radius // 2 - 4))
    set_rounded(card)
