from __future__ import annotations
from typing import Protocol

class ShapeFactory (Protocol):
    def create_circle(self) -> Circle:
        pass

    def create_square(self) -> Square:
        pass


class CircleFactory(ShapeFactory):
    def create_circle_a(self) -> CircleA:
        return 

    def create_circle_b(self) -> CircleB:
        return Square()