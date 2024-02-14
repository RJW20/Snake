
class Grid:
    """Grid that the game in played on."""

    __slots__ = (
        "size",
        "longest_edge",
        "block_width",
        "gridline_width",
        "board_size",
        "conversion_table",
    )

    def __init__(self, size, block_width, gridline_width):
        self.size = size
        self.longest_edge = max(size)
        self.block_width = block_width
        self.gridline_width = gridline_width

        #compute the board size
        self.board_size = tuple(gridline_width + self.size[i] * (block_width + gridline_width) for i in range(2))

        #set up a conversion table from grid point to x,y coordinates
        self.conversion_table = []
        for i in range(max(self.size)):
            self.conversion_table.append(gridline_width + i * (block_width + gridline_width))

    def getCoordinates(self, grid_position):
        """Get screen coordinates from gridpoints."""

        return(tuple(self.conversion_table[grid_position[i]] for i in range(2)))