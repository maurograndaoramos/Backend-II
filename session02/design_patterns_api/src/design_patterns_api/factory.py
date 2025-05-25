from design_patterns_api.shapes import Circle, Shape, Square

class ShapeFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ShapeFactory, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def create_shape(shape_type: str) -> Shape:
        if shape_type.lower() == "circle":
            return Circle()
        elif shape_type.lower() == "square":
            return Square()
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
         
if __name__ == "__main__":
    circle = ShapeFactory.create_shape("circle")
    print(circle.process())  

    square = ShapeFactory.create_shape("square")
    print(square.process())  

    try:
        unknown_shape = ShapeFactory.create_shape("triangle")
    except ValueError as e:
        print(e)  