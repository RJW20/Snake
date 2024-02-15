from functools import cached_property

class Grid:
    """Grid that the game in played on."""

    def __init__(self, size, block_width, gridline_width):
        self.size = size
        self.block_width = block_width
        self.gridline_width = gridline_width

    @cached_property
    def longest_edge(self):
        return max(self.size)
    
    @cached_property
    def board_size(self):
        return tuple(self.gridline_width + self.size[i] * (self.block_width + self.gridline_width) for i in range(2))
    
    @cached_property
    def conversion_table(self):
        """Conversion table from gridpoint to x,y coordinates."""
        table = []
        for i in range(self.longest_edge):
            table.append(self.gridline_width + i * (self.block_width + self.gridline_width))
        return table

    def gridpoint_to_coordinates(self, grid_point):
        """Get screen coordinates from gridpoints."""

        return(tuple(self.conversion_table[grid_point[i]] for i in range(2)))