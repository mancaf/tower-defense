import os
import constants as cst
from .tile import Tile, Decoration

class Map:
	"""
	Represents a 2D map made out of tiles.
	Ascending X : East
	Ascending Y : South
	map.tiles is a dict mapping each position to a Tile object
	"""
	def __init__(self, tiles=None, deco = None):
		if tiles is None:
			self.tiles = dict(((x, y), Tile(pos=(x*cst.TILE_SIZE + cst.SCREEN_WIDTH//2, y*cst.TILE_SIZE + cst.SCREEN_HEIGHT//2))) for x in range(width) for y in range(height))
		else:
			self.tiles = tiles
		if deco is None :
			self.deco = {}
		else :
			self.deco = deco

	@staticmethod
	def create_plain(category, tile_type, width, height):
		""" Creates a 'width'*'height' map with only one tiletype. """
		new_map = Map(width=width, height=height)
		for tile in new_map.tiles.values():
			tile.change(category, tile_type)
		return new_map

	@staticmethod
	def import_map(map_name):
		""" Imports a map 'map_name' from the static/maps folder. map_name must end with {} """.format(cst.MAP_EXT)

		print("\nImporting map '{}'...".format(map_name))
		if not map_name.endswith(cst.MAP_EXT):
			raise TypeError("Cannot import map with name {}. Map names must end with '{}'.".format(map_name, cst.MAP_EXT))

		# used to check later on that all values are present in map file
		found = {"DECORATION_TYPES" : False, "TILE_TYPES": False, "TILES_ARRAY": False , "DECORATION_COORDS" : False}

		# fetch values from the .map file
		with open(os.path.join(cst.MAPS_DIR, map_name), 'r') as mapfile:
			l = mapfile.readline().strip()
			while l != "END_OF_FILE":

				# if empty line, just skip it
				if l == "":
					l = mapfile.readline().strip()
					continue

				# fetch the decoration_types dictionnary
				elif l == "DECORATION_TYPES" :
					deco_types = {}
					l = mapfile.readline().strip()
					while l != "END":
						symbol, category, deco_type = l.split()
						deco_types[symbol] = (category, deco_type)
						l = mapfile.readline().strip()
					found["DECORATION_TYPES"] = True

				# fetch the tile_types dictionnary
				elif l == "TILE_TYPES":
					tile_types = {}
					l = mapfile.readline().strip()
					while l != "END":
						symbol, category, tile_type = l.split()
						tile_types[symbol] = (category, tile_type)
						l = mapfile.readline().strip()
					found["TILE_TYPES"] = True

				# fetch the symbolic tiles array
				elif l == "TILES_ARRAY":
					tiles_symb = []
					l = mapfile.readline().strip()
					while l != "END":
						tiles_symb.append(list(l))
						l = mapfile.readline().strip()
					# must transpose columns and rows
					tiles_symb = list(map(list, zip(*tiles_symb)))
					# check dimensions are OK with the ones declared
					assert len(tiles_symb) == cst.TERRAIN_TILE_WIDTH, "Widths do not correspond !"
					assert len(tiles_symb[0]) == cst.TERRAIN_TILE_HEIGHT, "Heights do not correspond !"
					found["TILES_ARRAY"] = True

				# fetch the decoration coordinates
				elif l == "DECORATION_COORDS" :
					deco_coords = []
					l = mapfile.readline().strip()
					while l != "END" :
						symbol,x,y = l.split('.')
						deco_coords.append([symbol, int(x), int(y)])
						l = mapfile.readline().strip()
					found["DECORATION_COORDS"] = True

				l = mapfile.readline().strip()

		# check that all values were successfully fetched
		for to_find, val in found.items():
			not_found = []
			if not val:
				not_found.append(to_find)
			if not_found:
				raise NameError("Could not import map {} as the following is missing :\n{}".format(map_name, not_found))

		# assign tiles to a dict from symbolic tiles
		tiles = {}
		for x in range(cst.TERRAIN_TILE_WIDTH):
			for y in range(cst.TERRAIN_TILE_HEIGHT):
				cat, tile_type = tile_types[tiles_symb[x][y]]
				tiles[x, y] = Tile(pos=(x*cst.TILE_PIXEL_SIZE, y*cst.TILE_PIXEL_SIZE), category=cat, tile_type=tile_type)

		# assing decoration objects to a list
		deco = []
		for d in deco_coords :
			cat, deco_type = deco_types[d[0]]
			print(cat,deco_type)
			deco.append(Decoration(pos=(d[1]*cst.TILE_PIXEL_SIZE//cst.TILE_SIZE, d[2]*cst.TILE_PIXEL_SIZE//cst.TILE_SIZE), category=cat, deco_type=deco_type))

		# we're done !
		print("Map import is successful !")
		return Map(tiles=tiles, deco = deco)

	def __getitem__(self, pos):
		""" Allows direct access to the tiles, e.g. some_map[x, y] instead of some_map.tiles[x][y]. If y is not passed (some_map[x]), returns the complete row some_map.tiles[x]. """
		if isinstance(pos, tuple):
			x, y = pos
			return self.tiles[x, y]
		else:
			x = pos
			return self.tiles[x, 0]

	def __setitem__(self, pos, tile):
		""" Allows direct replacement of a tile, e.g. some_map[x, y] = new_tile """
		self.tiles[pos] = tile

	def __iter__(self):
		""" Iterates over the map tiles, in descending depth (y) order. """
		tiles_list = [tile for tile in self.tiles.values()]
		tiles_list.sort(key=lambda tile: tile.pos[0] + tile.pos[1])
		for tile in tiles_list:
			yield tile

	def copy(self):
		return Map(width=self.width, height=self.height, tiles=self.tiles)
