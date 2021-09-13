class State:
    def __init__(self, index: int, x0: int, y0: int, x1: int, y1: int):
        self.index = index

        self._x0 = x0
        self.x0: State = None
        self.y0 = y0

        self._x1 = x1
        self.x1: State = None
        self.y1 = y1

    def __str__(self) -> str:
        return f"S{self.index} S{self.x0.index}/{self.y0} S{self.x1.index}/{self.y1}"
