from app.models.graph.relationship_rules import (
    RelationshipRules,
)


class RelationshipMatcher:

    @classmethod
    def match(
        cls,
        source,
        target,
    ):

        key = (

            source.entity_type,

            target.entity_type,

        )

        return RelationshipRules.RULES.get(
            key
        )