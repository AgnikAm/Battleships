import pygame
from pygame import Surface, Rect, image

from component import Component
from drawing import draw_text
from drawing import MENU_BACKGROUND, MENU_ICON, TEXT_BOX_BIG, DARK_BROWN, FORWARD_ICON, ALKHEMIKAL


class RulesScreen:
    surface: Surface
    width: int
    height: int
    background: Surface

    bar: Rect
    bar_image: Surface
    bar_image_rect: Rect

    menu: Rect
    menu_icon: Surface
    menu_icon_rect: Rect

    forward_icon: Surface
    forward_icon_rect: Rect
    backward_icon: Surface
    backward_icon_rect: Rect

    header: Component
    placement_rules: list[str]
    battle_rules: list[str]

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

        self.width, self.height = surface.get_size()

        self.background = pygame.transform.scale(
            pygame.image.load(MENU_BACKGROUND), 
            surface.get_size()
        )

        self.bar = Rect(
            self.surface.get_rect().centerx - self.height // 2,
            self.surface.get_rect().centery - self.height * 0.75 // 2,
            self.height,
            self.height * 0.75
        )

        self.bar_image = pygame.transform.scale(
            image.load(TEXT_BOX_BIG),
            (self.width * 0.65, self.width * 0.5)
        )

        self.bar_image_rect = self.bar_image.get_rect(
            center = self.bar.center
        )

        self.menu = Rect(
            self.width - self.width // 12,
            self.height - self.width // 12,
            self.width // 12,
            self.width // 12
        )

        self.menu_icon = pygame.transform.scale(
            image.load(MENU_ICON),
            (self.width * 0.06, self.width * 0.06)
        )

        self.menu_icon_rect = self.menu_icon.get_rect(
            center = (80, 940)
        )

        self.forward_icon = pygame.transform.scale(
            image.load(FORWARD_ICON),
            (self.width * 0.04, self.width * 0.04)
        )

        self.forward_icon_rect = self.menu_icon.get_rect(
            center = (1400, 890)
        )

        self.backward_icon = pygame.transform.flip(
            self.forward_icon,
            True,
            False
        )

        self.backward_icon_rect = self.menu_icon.get_rect(
            center = (530, 890)
        )

        self.header = draw_text(
            "Rules",
            ALKHEMIKAL,
            int(self.height * 0.08),
            DARK_BROWN,
            (self.bar.centerx, self.bar.top)
        )

        self.placement_rules = ["Arr matey! Ye find yerself on a treacherous 10 x 10 grid, ready to set",
                      "sail with yer fleet. Ye'll be placin' 10 ships of various lengths:",
                      "4, 3, 3, 2, 2, 2, 1, 1, 1, and 1.",
                      "",
                      "Remember, these ships must be placed in straight lines, and they",
                      " mustn't be touchin' each other's sides or corners, else ye be meetin'",
                      " Davy Jones sooner than ye'd like!",
                      "",
                      '''If ye be lookin' for a bit o' help, ye can press the "Auto Place"''',
                      "button to have the ships arranged for ye. But if ye fancy yerself",
                      "a true captain of the seas, ye can click the back arrow button",
                      "to rearrange yer fleet to yer likin'.",
                      "",
                      "Once all yer ships are set to sail, ye can set course for adventure",
                      "by clickin' the arrow in the lower right corner of the screen.",
                      "",
                      "Fair winds and followin' seas, me hearties!"
        ]

        self.battle_rules = ["Each skirmish be initiated by ye, the captain. Ye be choosin' a cell",
                             "on the board to lay yer attack upon.",
                             "",
                             "If yer cannonball be missin', the box will be marked in blue, and the",
                             '''cry of "miss" will echo across the seas.''',
                             "",
                             "Should ye land a hit on a single segment of a ship, the box'll be",
                             '''painted red, and the word "hit" shall ring out like a bell tollin' doom.''',
                             "",
                             "But if yer strike be mighty enough to send a ship to",
                             ''' Davy Jones' locker the word "sunken" shall be spoken, markin' the end''',
                             "of that vessel's voyage.",
                             "",
                             "The battle rages on 'til either ye or yer foe find yer ships",
                             "at the mercy of the depths."

        ]


    def draw(self, rules: list[str]) -> None:
        self.surface.blit(self.background, (0, 0))

        self.surface.blit(self.bar_image, self.bar_image_rect)

        self.header.blit(self.surface)

        for i in range(len(rules)):

            rule = draw_text(
                rules[i],
                ALKHEMIKAL,
                int(self.height * 0.04),
                DARK_BROWN,
                (self.bar.centerx, self.bar.top + int(self.height * 0.08) + i * int(self.height * 0.04))
            )

            rule.blit(self.surface)

        self.surface.blit(self.menu_icon, self.menu_icon_rect)

        if rules == self.placement_rules:
            self.surface.blit(self.forward_icon, self.forward_icon_rect)
        else:
            self.surface.blit(self.backward_icon, self.backward_icon_rect)
