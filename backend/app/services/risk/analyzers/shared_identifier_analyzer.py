"""
Shared Identifier Analyzer
"""

from __future__ import annotations

from collections import defaultdict

from app.models.graph.graph_metadata import GraphMetadata
from app.models.risk.risk_factor import RiskFactor

from .base_analyzer import BaseAnalyzer


class SharedIdentifierAnalyzer(BaseAnalyzer):

    IDENTIFIER_FIELDS = {

        "email",

        "phone",

        "mobile",

        "pan",

        "aadhaar",

        "passport",

        "ip",

        "device_id",

        "account_number",

    }

    @classmethod
    def analyze(
        cls,
        graph: GraphMetadata,
    ) -> list[RiskFactor]:

        lookup = defaultdict(list)

        for entity in graph.entities:

            properties = getattr(entity, "properties", {})

            for key, value in properties.items():

                if key.lower() not in cls.IDENTIFIER_FIELDS:

                    continue

                if value is None:

                    continue

                lookup[(key.lower(), str(value))].append(entity)

        factors = []

        for (field, value), entities in lookup.items():

            if len(entities) < 2:

                continue

            for entity in entities:

                factors.append(

                    RiskFactor(

                        name=f"Shared {field}",

                        score=70,

                        weight=0.20,

                        description=(
                            f"{field} '{value}' is shared by "
                            f"{len(entities)} entities."
                        ),

                        entity_label=getattr(entity, "label", None),

                        entity_identifier=getattr(
                            entity,
                            "identifier",
                            None,
                        ),

                    )

                )

        return factors