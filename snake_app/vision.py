from dataclasses import dataclass

from .distance import Distance, WallsDistance


@dataclass
class Vision:
    """Organization of snake's vision.
    
    If the head is next to a given point, the distance is considered to be 1.
    If the head can't see something, the distance is considered to be np.inf.
    """

    walls: WallsDistance
    food: Distance
    body: Distance