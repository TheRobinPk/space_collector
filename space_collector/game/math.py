from __future__ import annotations


class Vector:
    def __init__(self, data: list) -> None:
        self.data = list(data)

    def __repr__(self) -> str:
        return "Vector(" + ", ".join(str(item) for item in self.data) + ")"

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __add__(self, other: Vector) -> Vector:
        if isinstance(other, Vector):
            return Vector(s + o for s, o in zip(self, other))
        raise NotImplemented

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def z(self):
        return self.data[2]


class Matrix:
    def __init__(self, data: list) -> None:
        """First dimension in data is rows: [[a,b],[c,d]] => [a,b] is first row."""
        self.data = data

    def __getitem__(self, indices_tuple: tuple[int]):
        data = self.data
        indices = list(indices_tuple)
        while indices:
            data = data[indices.pop(0)]
        return data

    def __matmul__(self, other: Vector | Matrix) -> Vector | Matrix:
        assert isinstance(other, Vector)  # Matrix @ Matrix not implemented yet
        result = Vector([])
        for index in range(len(other)):
            result.data.append(
                sum(mat * vec for mat, vec in zip(self.data[index], other))
            )
        return result
