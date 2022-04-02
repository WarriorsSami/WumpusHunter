from settings import TILE_SIZE


class TextMap:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tile_width = len(self.data[0])
        self.tile_height = len(self.data)
        self.width = self.tile_width * TILE_SIZE
        self.height = self.tile_height * TILE_SIZE
