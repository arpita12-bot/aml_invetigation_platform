"""
==========================================================
AML Investigation Platform

Triple Validator

Responsibilities
----------------
✓ Validate triples
✓ Remove duplicates
✓ Detect invalid triples
✓ Generate validation statistics

==========================================================
"""

from __future__ import annotations

from app.models.knowledge_graph.triple import Triple


class TripleValidator:
    """
    Validates Knowledge Graph triples before they are exported
    for PyKEEN training.
    """

    @classmethod
    def validate(
        cls,
        triples: list[Triple],
    ) -> tuple[
        list[Triple],
        list[str],
        int,
    ]:
        """
        Returns
        -------
        (
            valid_triples,
            warnings,
            duplicate_count,
        )
        """

        valid_triples: list[Triple] = []

        warnings: list[str] = []

        seen: set[
            tuple[str, str, str]
        ] = set()

        duplicate_count = 0

        for triple in triples:

            # ----------------------------------
            # Head
            # ----------------------------------

            if not triple.head.strip():

                warnings.append(
                    "Missing head entity."
                )

                continue

            # ----------------------------------
            # Relation
            # ----------------------------------

            if not triple.relation.strip():

                warnings.append(
                    f"{triple.head}: missing relation."
                )

                continue

            # ----------------------------------
            # Tail
            # ----------------------------------

            if not triple.tail.strip():

                warnings.append(
                    f"{triple.head}: missing tail."
                )

                continue

            # ----------------------------------
            # Confidence
            # ----------------------------------

            if not (
                0.0 <= triple.confidence <= 1.0
            ):

                warnings.append(
                    f"Invalid confidence for "
                    f"{triple.as_tuple()}"
                )

                continue

            # ----------------------------------
            # Duplicate
            # ----------------------------------

            key = triple.as_tuple()

            if key in seen:

                duplicate_count += 1

                continue

            seen.add(key)

            # ----------------------------------
            # Self Loop
            # ----------------------------------

            if triple.head == triple.tail:

                warnings.append(
                    f"Self-loop detected: {key}"
                )

            valid_triples.append(triple)

        return (
            valid_triples,
            warnings,
            duplicate_count,
        )