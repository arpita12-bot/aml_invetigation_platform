from sqlalchemy.orm import Session

from app.models.graph_registry import GraphRegistry


class GraphRegistryService:

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------

    def get_active_tables(self):

        return (
            self.db.query(GraphRegistry)
            .filter(
                GraphRegistry.include_in_graph.is_(True),
                GraphRegistry.is_active.is_(True),
            )
            .order_by(GraphRegistry.table_name)
            .all()
        )

    # --------------------------------------------------

    def get_table(self, table_name: str):

        return (
            self.db.query(GraphRegistry)
            .filter(
                GraphRegistry.table_name == table_name
            )
            .first()
        )

    # --------------------------------------------------

    def register_table(
        self,
        *,
        table_name: str,
        node_label: str,
        identifier_column: str,
        display_column: str | None = None,
        entity_type: str | None = None,
    ):

        existing = self.get_table(table_name)

        if existing:
            return existing

        registry = GraphRegistry(
            table_name=table_name,
            node_label=node_label,
            identifier_column=identifier_column,
            display_column=display_column,
            entity_type=entity_type,
            include_in_graph=True,
            is_active=True,
        )

        self.db.add(registry)

        self.db.commit()

        self.db.refresh(registry)

        return registry