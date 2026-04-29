import math

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        """简单的加法"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def calculate_circle_area(self, radius):
        """计算圆形面积"""
        if radius < 0:
            raise ValueError("半径不能为负数")
        area = math.pi * (radius ** 2)
        self.history.append(f"Area of circle with radius {radius} is {area}")
        return area

    def get_history(self):
        return self.history
