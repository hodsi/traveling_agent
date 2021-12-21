import dataclasses


@dataclasses.dataclass
class Edge(object):
    source_vertex: int
    destination_vertex: int
