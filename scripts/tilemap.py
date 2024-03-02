import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone','floor', 'wall'}
PHYSICS_TILES1 = {'floor', 'wall'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = {}

        
    
        csv_file_path = r'C:\Users\Lolopenza\Desktop\Projects\game2\Level\level1.csv'
        self.csv_data = Tilemap.read_csv(csv_file_path)
    
        row_c = 0

        for row_c, row in enumerate(self.csv_data):
            for i, value in enumerate(row):
                if int(value) == -1:
                    pass
                elif int(value) == 0:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 0, 'pos': (i, row_c)}
                elif int(value) == 1:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 1, 'pos': (i, row_c)}
                elif int(value) == 2:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 2, 'pos': (i, row_c)}
                elif int(value) == 3:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 3, 'pos': (i, row_c)}
                elif int(value) == 4:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 4, 'pos': (i, row_c)}
                elif int(value) == 5:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 5, 'pos': (i, row_c)}
                elif int(value) == 6:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 6, 'pos': (i, row_c)}
                elif int(value) == 7:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 7, 'pos': (i, row_c)}
                elif int(value) == 8:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'grass', 'variant': 8, 'pos': (i, row_c)}
                elif int(value) == 10:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 0, 'pos': (i, row_c)}
                elif int(value) == 11:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 1, 'pos': (i, row_c)}
                elif int(value) == 12:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 2, 'pos': (i, row_c)}
                elif int(value) == 13:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 3, 'pos': (i, row_c)}
                elif int(value) == 14:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 4, 'pos': (i, row_c)}
                elif int(value) == 15:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 5, 'pos': (i, row_c)}
                elif int(value) == 16:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 6, 'pos': (i, row_c)}
                elif int(value) == 17:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 7, 'pos': (i, row_c)}
                elif int(value) == 18:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'stone', 'variant': 8, 'pos': (i, row_c)}
                elif int(value) == 20:
                    self.tilemap[str(i)+ ';' +str(row_c)] = {'type': 'decor', 'variant': 0, 'pos': (i, row_c)}
                elif int(value) == 21:
                    self.tilemap[str(i)+ ';' +str(row_c)] = {'type': 'decor', 'variant': 1, 'pos': (i, row_c)}
                elif int(value) == 22:
                    self.tilemap[str(i)+ ';' +str(row_c)] = {'type': 'decor', 'variant': 2, 'pos': (i, row_c)}
                elif int(value) == 23:
                    self.tilemap[str(i)+ ';' +str(row_c)] = {'type': 'decor', 'variant': 3, 'pos': (i, row_c)}
                elif int(value) == 24:
                    self.tilemap[str(i)+ ';' +str(row_c)] = {'type': 'large_decor', 'variant': 0, 'pos': (i, row_c)}
                elif int(value) == 25:
                    self.tilemap[str(i)+ ';' +str(row_c)] = {'type': 'large_decor', 'variant': 1, 'pos': (i, row_c)}
                elif int(value) == 26:
                    self.tilemap[str(i)+ ';' +str(row_c)] = {'type': 'large_decor', 'variant': 2, 'pos': (i, row_c + 0.25)}
        for i in range(20):
            self.tilemap[str(-1) + ';' + str(10+i)] = {'type': 'stone', 'variant': 1, 'pos': (-1, 10+i)}
        for i in range(20):
            self.tilemap[str(40) + ';' + str(10+i)] = {'type': 'stone', 'variant': 1, 'pos': (40, 10+i)}

        
    def read_csv(csv_file):
        data = []
        with open(csv_file, 'r') as f:
            rows = f.readlines()
            rows = list(map(lambda x:x.strip(), rows))

            for row in rows:
                row = row.split(',')
                data.append(row)

        return data
    
    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0]// self.tile_size ), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles 
    
    def physics_rects_around(self, pos):
        rects = []
        rect_off = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size , tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
            
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size  + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size  + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

class Tilemap2(Tilemap):
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = {}

        csv_file_path = r'C:\Users\Lolopenza\Desktop\Projects\game2\Level\level2.csv'
        self.csv_data = Tilemap2.read_csv(csv_file_path)

        for row_c, row in enumerate(self.csv_data):
            for i, value in enumerate(row):
                if int(value) == -1:
                    pass
                elif int(value) == 0:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'floor', 'variant': 0, 'pos': (i, row_c)}
                elif int(value) == 1:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'floor', 'variant': 1, 'pos': (i, row_c)}
                elif int(value) == 6:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'floor', 'variant': 2, 'pos': (i, row_c)}
                elif int(value) == 7:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'floor', 'variant': 3, 'pos': (i, row_c)}
                elif int(value) == 14:
                    self.tilemap[str(i)+ ';' + str(row_c)] = {'type': 'wall', 'variant': 0, 'pos': (i, row_c)}

    def tiles_around(self, pos):
        return super().tiles_around(pos)
    def physics_rects_around(self, pos):
        PHYSICS_TILES = PHYSICS_TILES1
        return super().physics_rects_around(pos)
    def solid_check(self, pos):
        PHYSICS_TILES = PHYSICS_TILES1
        return super().solid_check(pos) 
    def render(self, surf, offset=(0, 0)):
        return super().render(surf, offset)