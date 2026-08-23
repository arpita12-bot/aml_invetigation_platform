class RelationshipConfidence:

    @classmethod
    def score(
        cls,
        source,
        target,
    ) -> float:

        if source.primary_identifier:

            return 100.0

        return min(

            source.confidence,

            target.confidence,

        )