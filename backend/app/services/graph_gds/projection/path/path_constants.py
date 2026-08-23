"""
==========================================================
AML Investigation Platform

Path Analytics Constants

==========================================================
"""

# ----------------------------------------------------
# Neo4j Procedures
# ----------------------------------------------------

DIJKSTRA_PROCEDURE = "gds.shortestPath.dijkstra.stream"

ASTAR_PROCEDURE = "gds.shortestPath.astar.stream"

# ----------------------------------------------------
# Relationship Types
# ----------------------------------------------------

SHORTEST_PATH_RELATIONSHIP = "SHORTEST_PATH"

PEP_PATH_RELATIONSHIP = "PEP_PATH"

SANCTION_PATH_RELATIONSHIP = "SANCTION_PATH"

OWNERSHIP_PATH_RELATIONSHIP = "OWNERSHIP_PATH"

# ----------------------------------------------------
# Default Configuration
# ----------------------------------------------------

DEFAULT_MAX_DEPTH = 6

DEFAULT_BATCH_SIZE = 1000

DEFAULT_CONCURRENCY = 4

# ----------------------------------------------------
# Property Names
# ----------------------------------------------------

PATH_LENGTH_PROPERTY = "path_length"

RISK_SCORE_PROPERTY = "risk_score"

CREATED_AT_PROPERTY = "created_at"

UPDATED_AT_PROPERTY = "updated_at"