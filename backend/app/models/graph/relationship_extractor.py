"""
==========================================================
Relationship Extractor

==========================================================
"""

from app.models.schema.relationship_metadata import (
    RelationshipMetadata,
)

from app.models.graph.relationship_matcher import (
    RelationshipMatcher,
)

from app.models.graph.relationship_confidence import (
    RelationshipConfidence,
)


class RelationshipExtractor:

    @classmethod
    def extract(
        cls,
        entities,
    ):

        relationships = []

        for source in entities:

            for target in entities:

                if source == target:
                    continue

                relationship = RelationshipMatcher.match(

                    source,

                    target,

                )

                if relationship is None:
                    continue

                relationships.append(

                    RelationshipMetadata(

                        source=source.label,

                        target=target.label,

                        relationship_type=relationship,

                        confidence=RelationshipConfidence.score(

                            source,

                            target,

                        ),

                    )

                )

        return relationships