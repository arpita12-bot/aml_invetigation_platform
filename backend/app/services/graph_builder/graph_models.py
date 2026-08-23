from dataclasses import dataclass

@dataclass(slots=True)
class GraphStatistics:

    node_count: int

    relationship_count: int

    labels: dict[str, int]

    relationships: dict[str, int]