"""
==========================================================
AML Investigation Platform

Enterprise Entity Resolution Orchestrator

Responsibilities
----------------

✓ Coordinate complete entity resolution workflow

✓ Load datasets

✓ Generate blocking keys

✓ Produce candidate pairs

✓ Execute similarity matching

✓ Calculate confidence

✓ Persist mappings

✓ Synchronize Neo4j graph

✓ Produce execution statistics

✓ Support batch execution

✓ Support incremental execution

✓ Support rollback

==========================================================
"""

from __future__ import annotations

import logging
import traceback

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional

import pandas as pd


# ---------------------------------------------------------
# Engines
# ---------------------------------------------------------

from app.services.blocking_engine import BlockingEngine

from app.entity_resolution.services.candidate_generator import (
    CandidateGenerator,
)

from app.entity_resolution.services.similarity_engine import (
    SimilarityEngine,
)

from app.entity_resolution.services.confidence_engine import (
    ConfidenceEngine,
)

from app.entity_resolution.services.match_persistence import (
    MatchPersistenceEngine,
)

from app.entity_resolution.models.pipeline_results import (
    BlockingResult,
    CandidateResult,
    SimilarityResultSet,
    ConfidenceResultSet,
    PersistenceResult,
    GraphSyncResult,
)
# ---------------------------------------------------------
# Future Services
# ---------------------------------------------------------

# from app.graph.services.graph_sync_service import GraphSyncService
# from app.services.dataset_loader import DatasetLoader

logger = logging.getLogger(__name__)

class ResolutionStatus(str, Enum):

    CREATED = "CREATED"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"
    
@dataclass
class ResolutionConfiguration:
    """
    Runtime configuration.
    """

    batch_size: int = 1000

    similarity_batch_size: int = 500

    auto_commit: bool = True

    update_graph: bool = True

    persist_results: bool = True

    enable_statistics: bool = True

    stop_on_error: bool = True

    incremental: bool = False

    max_workers: int = 4

    verbose: bool = False
    
@dataclass
class ResolutionStatistics:
    """
    Runtime statistics.
    """

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    elapsed_seconds: float = 0.0

    customers_loaded: int = 0

    companies_loaded: int = 0

    blocking_candidates: int = 0

    candidate_pairs: int = 0

    similarity_results: int = 0

    matched_entities: int = 0

    review_queue: int = 0

    persisted: int = 0

    graph_nodes: int = 0

    graph_edges: int = 0

    errors: int = 0
    
@dataclass
class ResolutionContext:
    """
    Shared runtime context.
    """

    # Input datasets
    customers: Optional[pd.DataFrame] = None
    companies: Optional[pd.DataFrame] = None
    pep: Optional[pd.DataFrame] = None
    sanctions: Optional[pd.DataFrame] = None

    # Pipeline results
    blocking: Optional[BlockingResult] = None
    candidates: Optional[CandidateResult] = None
    similarity: Optional[SimilarityResultSet] = None
    confidence: Optional[ConfidenceResultSet] = None
    persistence: Optional[PersistenceResult] = None
    graph: Optional[GraphSyncResult] = None
    
class EntityResolutionOrchestrator:
    """
    Enterprise Entity Resolution Pipeline.
    """
    def __init__(
            self,
            dataset_loader,
            blocking_engine: BlockingEngine,
            candidate_generator: CandidateGenerator,
            similarity_engine: SimilarityEngine,
            confidence_engine: ConfidenceEngine,
            persistence_engine: MatchPersistenceEngine,
            graph_service=None,
            configuration: Optional[
                ResolutionConfiguration
            ] = None,
        ):
    
            self.dataset_loader = dataset_loader
    
            self.blocking_engine = blocking_engine
    
            self.candidate_generator = candidate_generator
    
            self.similarity_engine = similarity_engine
    
            self.confidence_engine = confidence_engine
    
            self.persistence_engine = persistence_engine
    
            self.graph_service = graph_service
    
            self.configuration = (
                configuration
                or ResolutionConfiguration()
            )
    
            self.statistics = ResolutionStatistics()
    
            self.context = ResolutionContext()
    
            logger.info(
                "Entity Resolution Orchestrator initialized."
            )
    
        
    def start(self) -> None:
        """
        Begin execution.
        """

        self.reset()

        self.statistics.started_at = datetime.utcnow()

        logger.info(
            "Entity Resolution started."
            )
        
    def finish(self) -> None:
        """
        Finish execution.
        """

        self.statistics.completed_at = datetime.utcnow()

        if self.statistics.started_at:

            self.statistics.elapsed_seconds = (

                self.statistics.completed_at
                - self.statistics.started_at

            ).total_seconds()

        logger.info(
            "Entity Resolution completed.",
            logger.info(
            "Pipeline Summary: %s",
            self.summary())
        )
        
        
    # ---------------------------------------------------------
    # Reset Pipeline
    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset runtime state before execution.
        """

        self.context = ResolutionContext()

        self.statistics = ResolutionStatistics()

        logger.info(
            "Entity Resolution state reset.",
            logger.info(
            "Pipeline Summary: %s",
            self.summary())
        )
    # -----------------------------------------------------
    # Load Customers
    # -----------------------------------------------------

    def load_customers(self) -> pd.DataFrame:
        """
        Load customer dataset.
        """

        logger.info("Loading customers...")

        customers = self.dataset_loader.load_table(
            "customers"
        )

        if customers is None:

            raise ValueError(
                "Customer dataset not found."
            )

        self.context.customers = customers

        self.statistics.customers_loaded = len(
            customers
        )

        logger.info(
            "Loaded %s customers.",
            len(customers),
        )

        return customers
    
    # -----------------------------------------------------
    # Load Companies
    # -----------------------------------------------------

    def load_companies(self) -> pd.DataFrame:
        """
        Load company dataset.
        """

        logger.info("Loading companies...")

        companies = self.dataset_loader.load_table(
            "companies"
        )

        if companies is None:

            companies = pd.DataFrame()

        self.context.companies = companies

        self.statistics.companies_loaded = len(
            companies
        )

        logger.info(
            "Loaded %s companies.",
            len(companies),
        )

        return companies
    
    # -----------------------------------------------------
    # Load PEP
    # -----------------------------------------------------

    def load_pep(self) -> pd.DataFrame:
        """
        Load PEP records.
        """

        logger.info("Loading PEP dataset...")

        pep = self.dataset_loader.load_table(
            "pep"
        )

        if pep is None:

            pep = pd.DataFrame()

        self.context.pep = pep

        return pep
    # -----------------------------------------------------
    # Load Sanctions
    # -----------------------------------------------------

    def load_sanctions(self) -> pd.DataFrame:
        """
        Load sanctions dataset.
        """

        logger.info("Loading sanctions...")

        sanctions = self.dataset_loader.load_table(
            "sanctions"
        )

        if sanctions is None:

            sanctions = pd.DataFrame()

        self.context.sanctions = sanctions

        return sanctions
        # -----------------------------------------------------
    # Load Datasets
    # -----------------------------------------------------

    def load_datasets(self) -> None:
        """
        Load all required datasets.
        """

        self.load_customers()

        self.load_companies()

        self.load_pep()

        self.load_sanctions()
        
    # -----------------------------------------------------
    # Validate Datasets
    # -----------------------------------------------------

    def validate_datasets(self) -> None:
        """
        Validate loaded datasets.
        """

        if self.context.customers is None:

            raise RuntimeError(
                "Customers were not loaded."
            )

        if self.context.customers.empty:

            raise RuntimeError(
                "Customer dataset is empty."
            )

        logger.info(
            "Datasets successfully validated."
        )
        # -----------------------------------------------------
    # Prepare Pipeline
    # -----------------------------------------------------

    def prepare(self) -> None:
        """
        Prepare pipeline execution.
        """

        self.start()

        self.load_datasets()

        self.validate_datasets()
        
    # ---------------------------------------------------------
    # Blocking Stage
    # ---------------------------------------------------------

    def execute_blocking(self) -> Dict[str, Any]:
        """
        Execute blocking phase.

        Returns
        -------
        Dict[str, Any]
            Blocking index produced by BlockingEngine.
        """

        logger.info(
            "Starting blocking stage..."
        )

        if self.context.customers is None:

            raise RuntimeError(
                "Customers dataset has not been loaded."
            )

        blocking_results = self.blocking_engine.generate_blocks(
            self.context.customers
        )

        if blocking_results is None:

            raise RuntimeError(
                "Blocking engine returned None."
            )

        self.context.blocking = blocking_results

        self.statistics.blocking_candidates = len(
            blocking_results
        )

        logger.info(
            "Blocking completed. %s blocks created.",
            len(blocking_results),
        )

        return blocking_results

    # ---------------------------------------------------------
    # Validate Blocking
    # ---------------------------------------------------------

    def validate_blocking(self) -> None:
        """
        Validate blocking results.
        """

        blocks = self.context.blocking

        if blocks is None:

            raise RuntimeError(
                "Blocking results missing."
            )

        if len(blocks) == 0:

            raise RuntimeError(
                "No blocking keys generated."
            )

        logger.info(
            "Blocking validation successful."
        )
    # ---------------------------------------------------------
    # Blocking Summary
    # ---------------------------------------------------------

    def blocking_summary(self) -> Dict[str, Any]:
        """
        Return blocking statistics.
        """

        blocks = self.context.blocking

        if not blocks:

            return {}

        largest_block = max(
            len(v)
            for v in blocks.values()
        )

        average_block_size = (
            sum(len(v) for v in blocks.values())
            / len(blocks)
        )

        return {

            "blocks": len(blocks),

            "largest_block": largest_block,

            "average_block_size": round(
                average_block_size,
                2,
            ),

        }
        
    # ---------------------------------------------------------
    # Log Blocking
    # ---------------------------------------------------------

    def log_blocking_statistics(self) -> None:
        """
        Log blocking metrics.
        """

        summary = self.blocking_summary()

        if not summary:

            return

        logger.info(
            "Blocking Statistics:"
        )

        logger.info(
            "Blocks              : %s",
            summary["blocks"],
        )

        logger.info(
            "Largest Block       : %s",
            summary["largest_block"],
        )

        logger.info(
            "Average Block Size  : %.2f",
            summary["average_block_size"],
        )
        
    # ---------------------------------------------------------
    # Run Blocking Stage
    # ---------------------------------------------------------

    def run_blocking(self) -> Dict[str, Any]:
        """
        Execute complete blocking stage.
        """

        blocks = self.execute_blocking()

        self.validate_blocking()

        self.log_blocking_statistics()

        return blocks
    
    # ---------------------------------------------------------
    # Candidate Generation
    # ---------------------------------------------------------

    def execute_candidate_generation(self) -> CandidateResult:
        """
        Generate candidate pairs from blocking results.
        """

        logger.info(
            "Starting candidate generation..."
        )

        if self.context.blocking is None:

            raise RuntimeError(
                "Blocking stage has not been executed."
            )

        blocking_result = self.context.blocking

        candidate_result = (
            self.candidate_generator.generate_candidates(
                blocking_result.block_index
            )
        )

        if candidate_result is None:

            raise RuntimeError(
                "Candidate Generator returned None."
            )

        self.context.candidates = candidate_result

        self.statistics.candidate_pairs = (
            candidate_result.total_candidates
        )

        logger.info(
            "Generated %s candidate pairs.",
            candidate_result.total_candidates,
        )

        return candidate_result
    
    # ---------------------------------------------------------
    # Validate Candidates
    # ---------------------------------------------------------

    def validate_candidates(self) -> None:
        """
        Validate generated candidate pairs.
        """

        if self.context.candidates is None:

            raise RuntimeError(
                "Candidate generation not executed."
            )

        if (
            self.context.candidates.total_candidates
            == 0
        ):

            raise RuntimeError(
                "No candidate pairs generated."
            )

        logger.info(
            "Candidate validation successful."
    )
        
    # ---------------------------------------------------------
    # Candidate Summary
    # ---------------------------------------------------------

    def candidate_summary(self) -> dict:
        """
        Candidate generation summary.
        """

        if self.context.candidates is None:

            return {}

        result = self.context.candidates

        return {

            "candidate_pairs":
                result.total_candidates,

            "duplicates_removed":
                result.duplicate_candidates_removed,

        }
        
    # ---------------------------------------------------------
    # Log Candidate Statistics
    # ---------------------------------------------------------

    def log_candidate_statistics(self) -> None:

        summary = self.candidate_summary()

        if not summary:

            return

        logger.info(
            "Candidate Statistics:"
        )

        logger.info(
            "Candidate Pairs      : %s",
            summary["candidate_pairs"],
        )

        logger.info(
            "Duplicates Removed   : %s",
            summary["duplicates_removed"],
        )
        
    # ---------------------------------------------------------
    # Run Candidate Generation
    # ---------------------------------------------------------

    def run_candidate_generation(
        self,
    ) -> CandidateResult:
        """
        Execute complete candidate generation stage.
        """

        result = self.execute_candidate_generation()

        self.validate_candidates()

        self.log_candidate_statistics()

        return result
    
    # ---------------------------------------------------------
    # Similarity Stage
    # ---------------------------------------------------------

    def execute_similarity(
        self,
    ) -> SimilarityResultSet:
        """
        Execute similarity engine.
        """

        logger.info(
            "Starting similarity calculation..."
        )

        if self.context.candidates is None:

            raise RuntimeError(
                "Candidate generation not completed."
            )

        similarity_result = self.similarity_engine.compare_candidates(
            candidates=self.context.candidates.candidate_pairs,
            records=self.context.customers.to_dict("records"),
        )

        if similarity_result is None:

            raise RuntimeError(
                "Similarity Engine returned None."
            )

        self.context.similarity = similarity_result

        self.statistics.similarity_results = (
            similarity_result.processed_pairs
        )

        logger.info(
            "Processed %s candidate pairs.",
            similarity_result.processed_pairs,
        )

        return similarity_result
    
    # ---------------------------------------------------------
    # Validate Similarity
    # ---------------------------------------------------------

    def validate_similarity(self):

        if self.context.similarity is None:

            raise RuntimeError(
                "Similarity stage not executed."
            )

        if (
            self.context.similarity.processed_pairs
            == 0
        ):

            raise RuntimeError(
                "No similarity results generated."
            )

        logger.info(
            "Similarity validation completed."
        )
        
    # ---------------------------------------------------------
    # Similarity Summary
    # ---------------------------------------------------------

    def similarity_summary(self):

        result = self.context.similarity

        if result is None:

            return {}

        return {

            "processed_pairs":
                result.processed_pairs,

            "matched_pairs":
                result.matched_pairs,

            "average_similarity":
                round(
                    result.average_similarity,
                    4,
                ),

            "highest_similarity":
                result.highest_similarity,

            "lowest_similarity":
                result.lowest_similarity,

            "processing_time":
                result.processing_time,

        }
        
    # ---------------------------------------------------------
    # Log Similarity Statistics
    # ---------------------------------------------------------

    def log_similarity_statistics(self):

        summary = self.similarity_summary()

        if not summary:

            return

        logger.info(
            "Similarity Statistics"
        )

        logger.info(
            "Processed Pairs : %s",
            summary["processed_pairs"],
        )

        logger.info(
            "Matched Pairs : %s",
            summary["matched_pairs"],
        )

        logger.info(
            "Average Score : %.4f",
            summary["average_similarity"],
        )

        logger.info(
            "Highest Score : %.4f",
            summary["highest_similarity"],
        )

        logger.info(
            "Lowest Score : %.4f",
            summary["lowest_similarity"],
        )

        logger.info(
            "Processing Time : %.2fs",
            summary["processing_time"],
        )
    
    # ---------------------------------------------------------
    # Run Similarity Stage
    # ---------------------------------------------------------

    def run_similarity(
        self,
    ) -> SimilarityResultSet:

        result = self.execute_similarity()

        self.validate_similarity()

        self.log_similarity_statistics()

        return result
    
    # ---------------------------------------------------------
    # Confidence Stage
    # ---------------------------------------------------------

    def execute_confidence(
        self,
    ) -> ConfidenceResultSet:
        """
        Execute confidence scoring.
        """

        logger.info(
            "Starting confidence scoring..."
        )

        if self.context.similarity is None:

            raise RuntimeError(
                "Similarity stage has not been completed."
            )

        confidence_result = (
            self.confidence_engine.score(
                self.context.similarity.results
            )
        )

        if confidence_result is None:

            raise RuntimeError(
                "Confidence Engine returned None."
            )

        self.context.confidence = confidence_result

        self.statistics.matched_entities = (
            confidence_result.automatic_matches
        )

        self.statistics.review_queue = (
            confidence_result.manual_review
        )

        logger.info(
            "Confidence scoring completed."
        )

        return confidence_result

    # ---------------------------------------------------------
    # Validate Confidence
    # ---------------------------------------------------------

    def validate_confidence(self) -> None:
        """
        Validate confidence results.
        """

        if self.context.confidence is None:

            raise RuntimeError(
                "Confidence stage not executed."
            )

        total = (

            self.context.confidence.automatic_matches

            +

            self.context.confidence.manual_review

            +

            self.context.confidence.rejected

        )

        if total == 0:

            raise RuntimeError(
                "Confidence engine produced no results."
            )

        logger.info(
            "Confidence validation successful."
        )
    # ---------------------------------------------------------
    # Confidence Summary
    # ---------------------------------------------------------

    def confidence_summary(
        self,
    ) -> dict:

        if self.context.confidence is None:

            return {}

        result = self.context.confidence

        return {

            "automatic_matches":
                result.automatic_matches,

            "manual_review":
                result.manual_review,

            "rejected":
                result.rejected,

            "total_results":
                len(result.results),

        }
        
    # ---------------------------------------------------------
    # Log Confidence Statistics
    # ---------------------------------------------------------

    def log_confidence_statistics(
        self,
    ) -> None:

        summary = self.confidence_summary()

        if not summary:

            return

        logger.info(
            "Confidence Statistics"
        )

        logger.info(
            "Automatic Matches : %s",
            summary["automatic_matches"],
        )

        logger.info(
            "Manual Review     : %s",
            summary["manual_review"],
        )

        logger.info(
            "Rejected          : %s",
            summary["rejected"],
        )

        logger.info(
            "Total Results     : %s",
            summary["total_results"],
        )
    # ---------------------------------------------------------
    # Run Confidence Stage
    # ---------------------------------------------------------

    def run_confidence(
        self,
    ) -> ConfidenceResultSet:
        """
        Execute complete confidence stage.
        """

        result = self.execute_confidence()

        self.validate_confidence()

        self.log_confidence_statistics()

        return result
    
    # ---------------------------------------------------------
    # Persistence Stage
    # ---------------------------------------------------------

    def execute_persistence(
        self,
    ) -> PersistenceResult:
        """
        Persist resolved entity mappings.
        """

        logger.info(
            "Starting persistence stage..."
        )

        if self.context.confidence is None:

            raise RuntimeError(
                "Confidence stage has not been completed."
            )

        persistence_result = (
            self.persistence_engine.persist(
                self.context.confidence.results
            )
        )

        if persistence_result is None:

            raise RuntimeError(
                "Persistence Engine returned None."
            )

        self.context.persistence = persistence_result

        self.statistics.persisted = (
            persistence_result.inserted
            +
            persistence_result.updated
        )

        logger.info(
            "Persistence completed."
        )

        return persistence_result
    # ---------------------------------------------------------
    # Validate Persistence
    # ---------------------------------------------------------

    def validate_persistence(
        self,
    ) -> None:
        """
        Validate persistence results.
        """

        if self.context.persistence is None:

            raise RuntimeError(
                "Persistence stage not executed."
            )

        total = (
            self.context.persistence.inserted
            +
            self.context.persistence.updated
        )

        if total == 0:

            logger.warning(
                "No entity mappings were persisted."
            )

        logger.info(
            "Persistence validation successful."
        )
    # ---------------------------------------------------------
    # Persistence Summary
    # ---------------------------------------------------------

    def persistence_summary(
        self,
    ) -> dict:

        if self.context.persistence is None:

            return {}

        result = self.context.persistence

        return {

            "inserted":
                result.inserted,

            "updated":
                result.updated,

            "review_records":
                result.review_records,

            "execution_time":
                result.execution_time,

        }
        
    # ---------------------------------------------------------
    # Log Persistence Statistics
    # ---------------------------------------------------------

    def log_persistence_statistics(
        self,
    ) -> None:

        summary = self.persistence_summary()

        if not summary:

            return

        logger.info(
            "Persistence Statistics"
        )

        logger.info(
            "Inserted Records : %s",
            summary["inserted"],
        )

        logger.info(
            "Updated Records  : %s",
            summary["updated"],
        )

        logger.info(
            "Review Records   : %s",
            summary["review_records"],
        )

        logger.info(
            "Execution Time   : %.2fs",
            summary["execution_time"],
        )
        
    # ---------------------------------------------------------
    # Run Persistence Stage
    # ---------------------------------------------------------

    def run_persistence(
        self,
    ) -> PersistenceResult:
        """
        Execute complete persistence stage.
        """

        result = self.execute_persistence()

        self.validate_persistence()

        self.log_persistence_statistics()

        return result
    
    # ---------------------------------------------------------
    # Graph Synchronization
    # ---------------------------------------------------------

    def execute_graph_sync(
        self,
    ) -> GraphSyncResult:
        """
        Synchronize resolved entities into Neo4j.
        """

        logger.info(
            "Starting graph synchronization..."
        )

        if self.context.persistence is None:

            raise RuntimeError(
                "Persistence stage has not been completed."
            )

        graph_result = (
            self.graph_sync_service.sync(
                self.context.confidence.results
            )
        )

        if graph_result is None:

            raise RuntimeError(
                "Graph synchronization failed."
            )

        self.context.graph = graph_result

        logger.info(
            "Graph synchronization completed."
        )

        return graph_result
    
    # ---------------------------------------------------------
    # Validate Graph Synchronization
    # ---------------------------------------------------------

    def validate_graph_sync(
        self,
    ) -> None:
        """
        Validate graph synchronization.
        """

        if self.context.graph is None:

            raise RuntimeError(
                "Graph synchronization not executed."
            )

        logger.info(
            "Graph synchronization validation successful."
        )
        
    # ---------------------------------------------------------
    # Graph Summary
    # ---------------------------------------------------------

    def graph_summary(
        self,
    ) -> dict:

        if self.context.graph is None:

            return {}

        result = self.context.graph

        return {

            "nodes_created":
                result.nodes_created,

            "relationships_created":
                result.relationships_created,

            "execution_time":
                result.execution_time,

        }
        
    # ---------------------------------------------------------
    # Graph Statistics
    # ---------------------------------------------------------

    def log_graph_statistics(
        self,
    ) -> None:

        summary = self.graph_summary()

        if not summary:

            return

        logger.info(
            "Graph Synchronization Statistics"
        )

        logger.info(
            "Nodes Created         : %s",
            summary["nodes_created"],
        )

        logger.info(
            "Relationships Created : %s",
            summary["relationships_created"],
        )

        logger.info(
            "Execution Time        : %.2fs",
            summary["execution_time"],
        )
  
    # ---------------------------------------------------------
    # Run Graph Synchronization
    # ---------------------------------------------------------

    def run_graph_sync(
        self,
    ) -> GraphSyncResult:
        """
        Execute complete graph synchronization stage.
        """

        result = self.execute_graph_sync()

        self.validate_graph_sync()

        self.log_graph_statistics()

        return result
    
    # ---------------------------------------------------------
    # Pipeline Summary
    # ---------------------------------------------------------

    def summary(self) -> dict:
        """
        Return execution summary.
        """

        return {

            "blocking":
                self.blocking_summary(),

            "similarity":
                self.similarity_summary(),

            "confidence":
                self.confidence_summary(),

            "persistence":
                self.persistence_summary(),

            "graph":
                self.graph_summary(),

        }