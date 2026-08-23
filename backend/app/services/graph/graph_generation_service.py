"""
==========================================================
AML Investigation Platform

Graph Generation Service

Responsibilities
----------------
✓ Discover graph relationships
✓ Extract graph entities
✓ Build GraphMetadata
✓ Load graph into Neo4j
✓ Return generation statistics

This service orchestrates graph generation but does
not contain graph loading or Cypher generation logic.

==========================================================
"""

from __future__ import annotations

import logging
import time

from sqlalchemy.orm import Session

from app.models.graph.graph_metadata import GraphMetadata

from app.services.graph.discovery.metadata_cache import MetadataCache
from app.services.graph.discovery.relationship_discovery_service import (
    RelationshipDiscoveryService,
)

from app.services.graph.graph_entity_extractor import (
    GraphEntityExtractor,
)

from app.services.graph.graph_metadata_builder import (
    GraphMetadataBuilder,
)

from app.services.graph.neo4j.graph_loader import GraphLoader

logger = logging.getLogger(__name__)


class GraphGenerationService:
    """
    Coordinates complete graph generation.

    Flow
    ----
    PostgreSQL
        ↓
    Relationship Discovery
        ↓
    Entity Extraction
        ↓
    Graph Metadata Builder
        ↓
    Graph Loader
        ↓
    Neo4j
    """

    def __init__(
        self,
        metadata_cache: MetadataCache,
        relationship_service: RelationshipDiscoveryService,
        entity_extractor: GraphEntityExtractor,
        metadata_builder: GraphMetadataBuilder,
        graph_loader: GraphLoader,
    ) -> None:

        self._cache = metadata_cache
        self._relationship_service = relationship_service
        self._entity_extractor = entity_extractor
        self._metadata_builder = metadata_builder
        self._graph_loader = graph_loader

    def generate(
        self,
        session: Session,
    ) -> dict:

        logger.info("Starting graph generation.")

        started = time.perf_counter()

        # -------------------------------------------------
        # Load metadata cache
        # -------------------------------------------------

        self._cache.load()

        # -------------------------------------------------
        # Discover relationships
        # -------------------------------------------------

        logger.info("Discovering graph relationships...")

        relationships = self._relationship_service.discover(
            self._cache
        )

        logger.info(
            "Discovered %d relationships.",
            len(relationships),
        )

        # -------------------------------------------------
        # Extract graph entities
        # -------------------------------------------------

        logger.info("Extracting graph entities...")

        entities = self._entity_extractor.extract(
            session=session,
            metadata_cache=self._cache,
        )

        logger.info(
            "Extracted %d graph entities.",
            len(entities),
        )

        # -------------------------------------------------
        # Build GraphMetadata
        # -------------------------------------------------

        logger.info("Building GraphMetadata...")

        graph: GraphMetadata = self._metadata_builder.build(
            entities=entities,
            relationships=relationships,
        )

        # -------------------------------------------------
        # Load into Neo4j
        # -------------------------------------------------

        logger.info("Loading graph into Neo4j...")

        self._graph_loader.load(graph)

        elapsed = round(
            time.perf_counter() - started,
            2,
        )

        logger.info(
            "Graph generation completed in %.2f seconds.",
            elapsed,
        )

        return {
            "success": True,
            "entities": len(entities),
            "relationships": len(relationships),
            "duration_seconds": elapsed,
        }