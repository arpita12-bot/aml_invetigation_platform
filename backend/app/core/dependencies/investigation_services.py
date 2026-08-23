"""
Investigation Service Dependencies
"""

from functools import lru_cache

from app.services.graph_gds.projection.path.path_job import (
    PathJob,
)

from app.services.investigation.evidence_collector import (
    EvidenceCollector,
)

from app.services.investigation.recommendation_engine import (
    RecommendationEngine,
)

from app.services.investigation.investigation_report_builder import (
    InvestigationReportBuilder,
)

from app.services.investigation.investigation_engine import (
    InvestigationEngine,
)

from app.core.dependencies.graph_services import (
    get_shell_pattern_materializer,
)

from app.services.investigation.intelligence.risk_engine import (
    RiskEngine,
)

@lru_cache
def get_path_job():

    return PathJob()


@lru_cache
def get_evidence_collector():

    return EvidenceCollector(

        path_job=get_path_job(),

        shell_materializer=get_shell_pattern_materializer(),

    )


@lru_cache
def get_recommendation_engine():

    return RecommendationEngine()


@lru_cache
def get_report_builder():

    return InvestigationReportBuilder()


@lru_cache
def get_investigation_engine():

    return InvestigationEngine(

        risk_engine=get_risk_engine(),

        evidence_collector=get_evidence_collector(),

        recommendation_engine=get_recommendation_engine(),

        report_builder=get_report_builder(),

    )
    
@lru_cache
def get_risk_engine():

    return RiskEngine()
    
