from typing import List

from entities.route import Route


class WeightsMatrix(object):
    def __init__(self, matrix_of_weights: List[List[int]]):
        matrix_rows = len(matrix_of_weights)
        for row in matrix_of_weights:
            if len(row) != matrix_rows:
                raise ValueError(f'{type(self)} only gets a square matrix')
        self.matrix_of_weights = matrix_of_weights

    def get_weight(self, i: int, j: int) -> int:
        return self.matrix_of_weights[i][j]

    def get_route_weight(self, route: Route) -> int:
        return sum(self.get_weight(edge.source_vertex, edge.destination_vertex) for edge in route.get_edges())

    def __contains__(self, item: int):
        return any(item in row for row in self.matrix_of_weights)

    def __iter__(self):
        for row in self.matrix_of_weights:
            yield from row

    def __len__(self):
        return len(self.matrix_of_weights)

    def __repr__(self):
        return f'WeightsMatrix<{repr(self.matrix_of_weights)}>'
