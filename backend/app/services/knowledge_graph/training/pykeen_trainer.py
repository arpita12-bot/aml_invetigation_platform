"""
==========================================================
AML Investigation Platform

PyKEEN Trainer

Responsibilities
----------------
✓ Convert DatasetSplit → TriplesFactory
✓ Execute PyKEEN pipeline
✓ Save trained model
✓ Build TrainingResult

==========================================================
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import numpy as np
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory

from app.models.knowledge_graph.dataset_split import DatasetSplit
from app.models.knowledge_graph.model_artifact import ModelArtifact
from app.models.knowledge_graph.training_config import TrainingConfig
from app.models.knowledge_graph.training_paths import TrainingPaths
from app.models.knowledge_graph.training_result import TrainingResult
from app.models.knowledge_graph.training_status import TrainingStatus

logger = logging.getLogger(__name__)


class PyKEENTrainer:
    """
    Enterprise trainer for Knowledge Graph Embeddings.
    """

    def train(
        self,
        dataset: DatasetSplit,
        config: TrainingConfig,
    ) -> TrainingResult:

        start_time = datetime.utcnow()

        training_result = None

        try:

            logger.info(
                "Starting PyKEEN training (%s)",
                config.model.value,
            )

            train_factory = self._create_factory(
                dataset.training.triples
            )

            validation_factory = self._create_factory(
                dataset.validation.triples
            )

            test_factory = self._create_factory(
                dataset.testing.triples
            )

            paths = self._create_training_paths(config)

            self._create_directories(paths)

            pipeline_result = self._run_pipeline(
                train_factory=train_factory,
                validation_factory=validation_factory,
                test_factory=test_factory,
                config=config,
            )

            self._save_model(
                pipeline_result,
                paths,
            )

            metrics = self._extract_metrics(
                pipeline_result
            )

            artifact = ModelArtifact(
                model_directory=paths.model_directory,
                model_file=paths.model_file,
                entity_embeddings=paths.entity_embedding_file,
                relation_embeddings=paths.relation_embedding_file,
                config_file=paths.config_file,
                metrics_file=paths.metrics_file,
                training_log=paths.log_file,
            )

            end_time = datetime.utcnow()

            training_result = TrainingResult(
                experiment_name=config.experiment_name,
                model=config.model,
                dataset_name=dataset.training.dataset_name,
                training_triples=dataset.training.total_triples,
                validation_triples=dataset.validation.total_triples,
                testing_triples=dataset.testing.total_triples,
                embedding_dimension=config.embedding_dimension,
                epochs=config.num_epochs,
                batch_size=config.batch_size,
                learning_rate=config.learning_rate,
                random_seed=config.random_seed,
                mean_rank=metrics.get("mean_rank"),
                mean_reciprocal_rank=metrics.get("mrr"),
                hits_at_1=metrics.get("hits_at_1"),
                hits_at_3=metrics.get("hits_at_3"),
                hits_at_10=metrics.get("hits_at_10"),
                training_loss=metrics.get("loss"),
                artifact=artifact,
                status=TrainingStatus.COMPLETED,
                started_at=start_time,
                finished_at=end_time,
                execution_time_seconds=(
                    end_time - start_time
                ).total_seconds(),
            )

            logger.info("Training completed successfully.")

            return training_result

        except Exception as ex:

            logger.exception("Training failed.")

            end_time = datetime.utcnow()

            training_result = TrainingResult(
                experiment_name=config.experiment_name,
                model=config.model,
                dataset_name=dataset.training.dataset_name,
                training_triples=dataset.training.total_triples,
                validation_triples=dataset.validation.total_triples,
                testing_triples=dataset.testing.total_triples,
                embedding_dimension=config.embedding_dimension,
                epochs=config.num_epochs,
                batch_size=config.batch_size,
                learning_rate=config.learning_rate,
                random_seed=config.random_seed,
                artifact=None,
                status=TrainingStatus.FAILED,
                started_at=start_time,
                finished_at=end_time,
                execution_time_seconds=(
                    end_time - start_time
                ).total_seconds(),
                errors=[str(ex)],
            )

            return training_result

    @staticmethod
    def _create_factory(triples) -> TriplesFactory:

        rows = np.asarray(
            [
                [t.head, t.relation, t.tail]
                for t in triples
            ],
            dtype=str,
        )

        return TriplesFactory.from_labeled_triples(rows)

    @staticmethod
    def _create_training_paths(
        config: TrainingConfig,
    ) -> TrainingPaths:

        return TrainingPaths(
            root_directory=config.root_output_directory,
            experiment_name=config.experiment_name,
        )

    @staticmethod
    def _create_directories(
        paths: TrainingPaths,
    ) -> None:

        directories = [
            paths.model_directory,
            paths.embedding_directory,
            paths.metrics_directory,
            paths.config_directory,
            paths.log_directory,
        ]

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    @staticmethod
    def _run_pipeline(
        *,
        train_factory,
        validation_factory,
        test_factory,
        config,
    ):

        return pipeline(
            training=train_factory,
            validation=validation_factory,
            testing=test_factory,
            model=config.model.value,
            model_kwargs=dict(
                embedding_dim=config.embedding_dimension,
            ),
            training_kwargs=dict(
                num_epochs=config.num_epochs,
                batch_size=config.batch_size,
            ),
            optimizer_kwargs=dict(
                lr=config.learning_rate,
            ),
            random_seed=config.random_seed,
            device=config.device,
        )

    @staticmethod
    def _save_model(
        pipeline_result,
        paths: TrainingPaths,
    ) -> None:

        pipeline_result.save_to_directory(
            paths.model_directory
        )

    @staticmethod
    def _extract_metrics(
        pipeline_result,
    ) -> dict:

        metrics = {}

        try:
            metric_results = pipeline_result.metric_results

            metrics["mean_rank"] = getattr(
                metric_results,
                "mean_rank",
                None,
            )

            metrics["mrr"] = getattr(
                metric_results,
                "mean_reciprocal_rank",
                None,
            )

            metrics["hits_at_1"] = getattr(
                metric_results,
                "hits_at_1",
                None,
            )

            metrics["hits_at_3"] = getattr(
                metric_results,
                "hits_at_3",
                None,
            )

            metrics["hits_at_10"] = getattr(
                metric_results,
                "hits_at_10",
                None,
            )

        except Exception:

            logger.warning(
                "Unable to extract evaluation metrics."
            )

        metrics["loss"] = None

        return metrics