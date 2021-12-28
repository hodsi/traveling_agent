from typing import List

from entities.edge import Edge


class Route(object):
    def __init__(self, vertexes: List[int] = None, edges: List[Edge] = None, is_circle=False):
        self.is_circle = is_circle
        if [vertexes, edges].count(None) != 1:
            raise ValueError(f'{type(self)} gets either vertexes or edges')
        if edges:
            vertexes = [edges[0].source_vertex, edges[0].destination_vertex]
            for edge, next_edge in zip(edges[:-1], edges[1:]):
                if edge.destination_vertex != next_edge.source_vertex:
                    raise ValueError('these edges don\'t make a route')
                vertexes.append(next_edge.destination_vertex)
            if self.is_circle:
                if vertexes[0] != vertexes[-1]:
                    raise ValueError('If you create a circle the edges must create a circle')
                vertexes.pop()
        self.vertexes = vertexes

    def add_vertex(self, vertex: int):
        self.vertexes.append(vertex)

    def add_edge(self, edge: Edge):
        if edge.source_vertex != self.vertexes[-1]:
            raise ValueError('this edge is not a continuous of this route')
        self.vertexes.append(edge.destination_vertex)

    def get_edges(self):
        edges = [Edge(source, destination) for source, destination in zip(self.vertexes[:-1], self.vertexes[1:])]
        if self.is_circle:
            edges.append(Edge(self.vertexes[-1], self.vertexes[0]))
        return edges

    def __len__(self):
        return len(self.vertexes)

    def __repr__(self):
        if self.is_circle:
            return f'Circle<{self.vertexes + [self.vertexes[0]]}>'
        return f'Route<{repr(self.vertexes)}>'
