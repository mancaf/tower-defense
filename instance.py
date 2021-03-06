# encoding=utf-8

# ------ Importations ------

import pygame
from time import time
import constants as cst
import gui
from tiles.map import Map
from entities import moblist, turretlist, mainTurret
from isometric import isoutils
import time

# ------ Classe Principale ------

# key_to_function and button_to_function : simple mapping from keys and mouse buttons to Instance's functions
key_to_function = {
    pygame.K_LEFT: lambda self, event: self.rotate_all("left"),
    pygame.K_RIGHT: lambda self, event: self.rotate_all("right"),
    pygame.K_ESCAPE : lambda self, event: self.quit()
}
button_to_function = {
    1: lambda: None,  # left button
    3:  lambda: None,  # right button
}


class Instance:
    """
    Runs a game instance !
    """
    def __init__(self, map_name="basic.map"):
        # init pygame, screen and clock
        pygame.init()
        self.screen = cst.SCREEN
        self.clock = pygame.time.Clock()
        self.screen_width = cst.SCREEN_WIDTH
        self.screen_height = cst.SCREEN_HEIGHT

        # init the GUI
        self.gui = gui.game.GUI()

        # init the map
        self.map = Map.import_map(map_name)
        self.matrix = [[None for j in range(2*cst.MAP_WIDTH)] for i in range(2*cst.MAP_WIDTH)]

        # init turrets
        self.turrets = pygame.sprite.Group()
        self.player = mainTurret.MainTurret()
        self.turrets.add(self.player)

        # init the mobs
        self.mobs = pygame.sprite.Group()
        self.mobs.add(moblist.ChaserMob(tile_pos=(9, 12), target=self.map.tiles[1, 0]))
        self.mobs.add(moblist.ChaserMob(tile_pos=(12, 9), target=self.map.tiles[5, 2]))

        self.RUNNING = True

    def update(self, mouse_event, click_event):
        self.mobs.update()
        self.turrets.update()
        gui_update_dict = self.gui.update(mouse_event, click_event)
        self.place_turret(mouse_event, click_event, gui_update_dict["placed_turret"])

    def place_turret(self, mouse_event, click_event, turret):
        if turret is None:
            return
        elif turret == "placing":
            if mouse_event:
                # placing a turret and the mouse moved, check for new undertile
                undertile = None
                for tile in self.map.tiles.values():
                    if isoutils.iso_to_tile(*tile.iso_pos) == isoutils.iso_to_tile(*mouse_event.pos):
                        undertile = tile
                        break
                self.gui.undertile = undertile
        elif click_event:  # clicked to place turret
            turret.iso_pos = isoutils.tile_to_iso(isoutils.iso_to_tile(*click_event.pos))  # clip turret to mouse's pos on tiles map
            self.turrets.add(turret)
            self.gui.undertile = None

    def rotate_all(self, direction):
        """ Rotates the map by 90 degrees (clockwise if direction is 'left', counter-clockwise if direction is 'right') """
        func = "rotate_{}".format(direction)
        for tile in self.map.tiles.values():
            getattr(tile, func)()
        for mob in self.mobs:
            getattr(mob, func)()
        for deco in self.map.deco:
            getattr(deco, func)()
        for turret in self.turrets:
            getattr(turret, func)()

    def display(self):
        self.screen.fill(cst.PAPER)
        for tile in self.map.get_tiles():
            tile.display(self.screen)
        self.gui.display(self.screen)
        for deco in self.map.deco:
            deco.display(self.screen)
        for mob in self.mobs:
            mob.display(self.screen)
        for turret in self.turrets:
            turret.display(self.screen)

        # DEBUG
        if cst.DEBUG :
            # mid-screen lines
            pygame.draw.line(self.screen, pygame.Color("red"), (self.screen_width//2, 0), (self.screen_width//2, self.screen_height))
            pygame.draw.line(self.screen, pygame.Color("blue"), (0, self.screen_height//2), (self.screen_width, self.screen_height//2))

    def run(self):
        fps_counter = gui.misc.FpsCounter(nframes=40)  # handling fps print
        while self.RUNNING:
            self.clock.tick(cst.FPS)
            t = time.time()
            click_event = None
            mouse_event = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "PYGAME_QUIT"
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self, event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 3):
                        click_event = event
                elif event.type == pygame.MOUSEMOTION:
                    mouse_event = event
            self.update(mouse_event, click_event)
            self.display()
            pygame.display.flip()
            fps_counter.update(time.time()-t)

    def quit(self):
        self.RUNNING = False
