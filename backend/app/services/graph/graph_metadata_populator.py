from sqlalchemy.orm import Session

from app.models.schema.dataset_metadata import DatasetMetadata

from backend.app.services.graph.graph_entity_extractor import (
    GraphEntityExtractor,
)

from app.services.graph.graph_relationship_extractor import (
    GraphRelationshipExtractor,
)


class GraphMetadataPopulator:

    @classmethod
    def populate(
        cls,
        *,
        session: Session,
        metadata: DatasetMetadata,
    ) -> DatasetMetadata:

        entity_extractor = GraphEntityExtractor(session)

        relationship_extractor = (
            GraphRelationshipExtractor()
        )

        entities = entity_extractor.extract(

            table_name=metadata.table.table_name,

            node_label=metadata.graph.graph_name,

            identifier_property=(
                metadata.table.primary_key
            ),

        )

        relationships = (
            relationship_extractor.extract(
                entities
            )
        )

        metadata.graph.entities = entities

        metadata.graph.relationships = (
            relationships
        )

        return metadata