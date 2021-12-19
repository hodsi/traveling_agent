import dataclasses
from typing import List


@dataclasses.dataclass
class Edge(object):
    source_vertex: int
    destination_vertex: int


class Route(object):
    def __init__(self, vertexes: List[int] = None, edges: List[Edge] = None):
        if None not in (vertexes, edges):
            raise ValueError(f'{type(self)} gets either vertexes or edges, not both')
        if edges:
            vertexes = [edges[0].source_vertex, edges[0].destination_vertex]
            for edge, next_edge in zip(edges[:-1], edges[1:]):
                if edge.destination_vertex != next_edge.source_vertex:
                    raise ValueError('these edges don\'t make a route')
                vertexes.append(next_edge.destination_vertex)
        self.vertexes = vertexes

    def __repr__(self):
        return f'Route<{repr(self.vertexes)}>'


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
        return sum(self.get_weight(i, j) for i, j in zip(route.vertexes[:-1], route.vertexes[1:]))
