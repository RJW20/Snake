from functools import cached_property

class Grid:
    """Grid that the game in played on."""

    def __init__(self, size, block_width, block_padding):
        self.size = size
        self.block_width = block_width
        self.block_padding = block_padding

    @cached_property
    def longest_edge(self):
        return max(self.size)
    
    @cached_property
    def board_size(self):
        return tuple(self.block_padding + self.size[i] * (self.block_width + self.block_padding) for i in range(2))
    
    @cached_property
    def conversion_table(self):
        """Conversion table from gridpoint to x,y coordinates."""
        table = []
        for i in range(self.longest_edge):
            table.append(self.block_padding + i * (self.block_width + self.block_padding))
        return table

    def gridpoint_to_coordinates(self, grid_point):
        """Get screen coordinates from gridpoints."""

        return(tuple(self.conversion_table[grid_point[i]] for i in range(2)))