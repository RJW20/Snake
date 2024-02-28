from functools import cached_property

from cartesian import Point

class Grid:
    """Grid that the game in played on."""

    def __init__(self, size: tuple[int, int], block_width: int, block_padding: int) -> None:
        self.size: tuple[int, int] = size
        self.block_width: int = block_width
        self.block_padding: int = block_padding

    @cached_property
    def longest_edge(self) -> int:
        return max(self.size)
    
    @cached_property
    def screen_size(self) -> tuple[int, int]:
        """The size of the screen (in pixels) that corresponds the the grid's attributes."""

        return tuple(self.block_padding + self.size[i] * (self.block_width + self.block_padding) for i in range(2))
    
    @cached_property
    def conversion_table(self) -> list[int]:
        """Conversion table from gridpoint to (x, y) pixel coordinates."""

        table = []
        for i in range(self.longest_edge):
            table.append(self.block_padding + i * (self.block_width + self.block_padding))
        return table

    def gridpoint_to_coordinates(self, grid_point: Point) -> tuple[int, int]:
        """Get screen pixel coordinates from gridpoint."""

        return self.conversion_table[grid_point.x], self.conversion_table[grid_point.y]