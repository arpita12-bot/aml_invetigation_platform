"""
==========================================================
AML Investigation Platform

Investigation Composition Root

Responsibilities
----------------
✓ Construct investigation dependencies
✓ Wire repositories
✓ Wire services
✓ Build controller

==========================================================
"""

from __future__ import annotations

from app.api.investigation.controller import InvestigationController

from app.services.graph.neo4j.neo4j_connection import Neo4jConnection

from app.services.graph_gds.projection.graph_projection_repository import (
    GraphProjectionRepository,
)
from app.services.graph_gds.projection.graph_projection_service import (
    GraphProjectionService,
)

from app.services.graph_gds.projection.path.repositories.pep_path_repository import (
    PepPathRepository,
)
from app.services.graph_gds.projection.path.repositories.sanction_path_repository import (
    SanctionPathRepository,
)
from app.services.graph_gds.projection.path.repositories.ownership_path_repository import (
    OwnershipPathRepository,
)
from app.services.graph_gds.projection.path.repositories.shell_path_repository import (
    ShellPathRepository,
)
from app.services.graph_gds.projection.path.path_job import (
    PathJob,
)

from app.services.shell_detection.shell_pattern_repository import (
    ShellPatternRepository,
)
from app.services.shell_detection.shell_pattern_scoring import (
    ShellPatternScoring,
)
from app.services.shell_detection.shell_pattern_explainer import (
    ShellPatternExplainer,
)
from app.services.shell_detection.shell_pattern_materializer import (
    ShellPatternMaterializer,
)

from app.services.investigation.evidence_collector import (
    EvidenceCollector,
)
from app.services.investigation.services.investigation_service import (
    InvestigationService,
)


class InvestigationContainer:

    @classmethod
    def build_controller(cls) -> InvestigationController:

        evidence_collector = cls._build_evidence_collector()

        service = InvestigationService(
            evidence_collector=evidence_collector,
        )

        return InvestigationController(service)

    # ----------------------------------------------------
    # Driver
    # ----------------------------------------------------

    @staticmethod
    def _driver():

        return Neo4jConnection.driver()

    # ----------------------------------------------------
    # Graph Projection
    # ----------------------------------------------------

    @classmethod
    def _projection_service(cls):

        repository = GraphProjectionRepository(
            cls._driver(),
        )

        return GraphProjectionService(
            repository,
        )

    # ----------------------------------------------------
    # Path Analytics
    # ----------------------------------------------------

    @classmethod
    def _path_job(cls):

        driver = cls._driver()

        return PathJob(

            projection_service=cls._projection_service(),

            pep_repository=PepPathRepository(driver),

            sanction_repository=SanctionPathRepository(driver),

            ownership_repository=OwnershipPathRepository(driver),

            shell_repository=ShellPathRepository(driver),

        )

    # ----------------------------------------------------
    # Shell Detection
    # ----------------------------------------------------

    @classmethod
    def _shell_materializer(cls):

        repository = ShellPatternRepository(
            cls._driver(),
        )

        return ShellPatternMaterializer(

            repository=repository,

            scoring=ShellPatternScoring(),

            explainer=ShellPatternExplainer(),

        )

    # ----------------------------------------------------
    # Evidence Collector
    # ----------------------------------------------------

    @classmethod
    def _build_evidence_collector(cls):

        return EvidenceCollector(

            path_job=cls._path_job(),

            shell_materializer=cls._shell_materializer(),

        )