from abc import ABC

class Shape(ABC):
    def process(self):
        pass

class Circle (Shape):
    def process(self):
        return "Factory output: Circle"


class Square (Shape):
    def process(self):
        return "Factory output: Square"