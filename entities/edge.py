import dataclasses


@dataclasses.dataclass
class Edge(object):
    source_vertex: int
    destination_vertex: int

    def __repr__(self):
        return f'{self.source_vertex}->{self.destination_vertex}'
