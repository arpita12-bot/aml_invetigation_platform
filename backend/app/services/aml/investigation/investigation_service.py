"""
==========================================================
AML Investigation Platform

Investigation Service

Responsibilities
----------------

✓ Execute complete AML investigation
✓ Orchestrate all AML services
✓ Return investigation results

==========================================================
"""

from __future__ import annotations

import time

from app.models.aml.investigation_item import (
    InvestigationItem,
)

from app.models.aml.investigation_result import (
    InvestigationResult,
)

from app.models.prediction.prediction_request import (
    PredictionRequest,
)

from app.services.knowledge_graph.prediction.link_predictor import (
    PredictionService,
)

from app.services.aml.risk_scoring.risk_scoring_service import (
    RiskScoringService,
)

from app.services.aml.risk_scoring.shell_company_detector import (
    ShellCompanyDetector,
)

from app.services.aml.risk_scoring.relationship_explainer import (
    RelationshipExplainer,
)

from app.services.aml.recommendation.investigation_recommender import (
    InvestigationRecommender,
)

class InvestigationService:

    def __init__(
        self,
        prediction_service: PredictionService,
        risk_service: RiskScoringService,
        shell_detector: ShellCompanyDetector,
        explainer: RelationshipExplainer,
        recommender: InvestigationRecommender,
    ):

        self._prediction_service = prediction_service

        self._risk_service = risk_service

        self._shell_detector = shell_detector

        self._explainer = explainer

        self._recommender = recommender

    def investigate(
        self,
        request: PredictionRequest,
    ) -> InvestigationResult:

        started = time.perf_counter()

        prediction_result = (
            self._prediction_service.predict(request)
        )

        investigation_items = []

        for candidate in prediction_result.candidates:

            #
            # Placeholder values.
            #
            # In the next phase these will be
            # retrieved from Neo4j and PostgreSQL.
            #

            customer_score = 70

            company_score = 80

            graph_score = 75

            transaction_score = 68

            shared_directors = 2

            shared_addresses = 1

            shared_phone_numbers = 1

            shared_devices = 0

            circular_transactions = 3

            community_score = 82

            recent_registration = True

            risk = self._risk_service.calculate(

                prediction=candidate,

                customer_score=customer_score,

                company_score=company_score,

                graph_score=graph_score,

                transaction_score=transaction_score,
            )

            shell = self._shell_detector.assess(

                prediction=candidate,

                shared_directors=shared_directors,

                shared_addresses=shared_addresses,

                shared_phone_numbers=shared_phone_numbers,

                shared_devices=shared_devices,

                circular_transactions=circular_transactions,

                recent_registration=recent_registration,

                community_score=community_score,
            )

            explanation = self._explainer.explain(

                prediction=candidate,

                shared_directors=shared_directors,

                shared_addresses=shared_addresses,

                shared_phone_numbers=shared_phone_numbers,

                shared_devices=shared_devices,

                circular_transactions=circular_transactions,

                community_score=community_score,
            )

            recommendation = self._recommender.recommend(

                risk=risk,

                shell=shell,
            )

            investigation_items.append(

                InvestigationItem(

                    prediction=candidate,

                    risk=risk,

                    shell=shell,

                    explanation=explanation,

                    recommendation=recommendation,
                )
            )

        return InvestigationResult(

            items=investigation_items,

            execution_time_seconds=round(
                time.perf_counter() - started,
                3,
            ),

            warnings=[],

            errors=[],
        )