from dataclasses import dataclass

import numpy as np


@dataclass
class Distance:
    """Organization of distance to body or food."""

    f: int = np.inf
    fr: int = np.inf
    r: int = np.inf
    br: int = np.inf
    b: int = np.inf
    bl: int = np.inf
    l: int = np.inf
    fl: int = np.inf


class WallsDistance(Distance):
    """Organization of distance to walls."""

    def set_ordinals(self):
        """Set ordinal wall vision."""

        self.fr = min(self.f, self.r)
        self.br = min(self.b, self.r)
        self.bl = min(self.b, self.l)
        self.fl = min(self.f, self.l)

    def turn_right(self):
        """Simulate a right turn."""

        #save 2 of the directions
        old_f = self.f
        old_fr = self.fr

        #update all the directions
        self.f = self.r
        self.fr = self.br
        self.r = self.b
        self.br = self.bl
        self.b = self.l
        self.bl = self.fl
        self.l = old_f
        self.fl = old_fr

    def turn_left(self):
        """Simulate a left turn."""

        #save 2 of the directions
        old_f = self.f
        old_fl = self.fl

        #update all the directions
        self.f = self.l
        self.fl = self.bl
        self.l = self.b
        self.bl = self.br
        self.b = self.r
        self.br = self.fr
        self.r = old_f
        self.fr = old_fl