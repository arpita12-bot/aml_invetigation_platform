from dataclasses import dataclass


@dataclass(slots=True)
class SimilarityExecutionPlan:

    similarity_threshold: float = 0.80

    top_k: int = 10

    write_relationship: bool = True