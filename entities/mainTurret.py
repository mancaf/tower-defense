# encoding=utf-8

# ------ Importations ------

import pygame
import math
import os
from isometric import IsoSprite
import constants as cst
from . import turret


class MainTurret(turret.Turret):
    """
    The Main tower in the middle of the battle field.
    This class also contains every datas related to the player, like money or score.
    """
    def __init__(self):
        super(MainTurret, self).__init__(path_to_image=["turrets", "maintower.png"], tile_pos=(0,0))
        self.hp = 1000
        self.money = 400
        self.score = 0

        # Data redefinition
        self.name = "Main Tower"
        self.nameb.change_message(self.name)
        self.hb.rect.width = 3*self.hb.rect.width