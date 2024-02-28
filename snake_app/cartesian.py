from __future__ import annotations
from enum import Enum


class Point:
    """(x, y) point on the grid."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Point | Slope) -> Point:
        if isinstance(other, Point):
            diff_x = self.x + other.x
            diff_y = self.y + other.y
        elif isinstance(other, Slope):
            diff_x = self.x + other.run
            diff_y = self.y + other.rise
        return Point(diff_x, diff_y)
    
    def __sub__(self, other: Point | Slope) -> Point:
        if isinstance(other, Point):
            diff_x = self.x - other.x
            diff_y = self.y - other.y
        elif isinstance(other, Slope):
            diff_x = self.x - other.run
            diff_y = self.y - other.rise
        return Point(diff_x, diff_y)
    
    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y


class Slope:
    """(d_x, d_y) vector on the grid."""

    def __init__(self, run: int, rise: int) -> None:
        self.run = run
        self.rise = rise


class Direction(Enum):
    """Possible directions for snake to travel in."""

    N = Slope(0, -1)
    E = Slope(1, 0)
    S = Slope(0, 1)
    W = Slope(-1, 0)
