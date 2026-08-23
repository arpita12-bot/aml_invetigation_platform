"""
==========================================================
AML Investigation Platform

Similarity Constants

Centralized configuration for Neo4j Graph Data Science
Similarity algorithms.

==========================================================
"""

from __future__ import annotations

# ==========================================================
# Relationship Configuration
# ==========================================================

SIMILAR_RELATIONSHIP_TYPE = "SIMILAR_TO"

SIMILARITY_SCORE_PROPERTY = "score"


# ==========================================================
# Default Execution Configuration
# ==========================================================

DEFAULT_SIMILARITY_THRESHOLD = 0.80

DEFAULT_TOP_K = 10

DEFAULT_WRITE_RELATIONSHIPS = True


# ==========================================================
# Supported Similarity Algorithms
# ==========================================================

NODE_SIMILARITY_PROCEDURE = "gds.nodeSimilarity.write"

JACCARD_SIMILARITY_PROCEDURE = "gds.nodeSimilarity.filtered.write"

COSINE_SIMILARITY_PROCEDURE = "gds.knn.write"


# ==========================================================
# Future Relationship Types
# ==========================================================

POTENTIAL_SHELL_RELATIONSHIP = "POTENTIAL_SHELL"

POTENTIAL_DUPLICATE_RELATIONSHIP = "POTENTIAL_DUPLICATE"

POTENTIAL_MULE_RELATIONSHIP = "POTENTIAL_MULE"

POTENTIAL_BENEFICIAL_OWNER = "POTENTIAL_BENEFICIAL_OWNER"


# ==========================================================
# Similarity Labels
# (Restrict comparisons to same entity type)
# ==========================================================

CUSTOMER_LABEL = "Customer"

COMPANY_LABEL = "Company"

ACCOUNT_LABEL = "Account"

DEVICE_LABEL = "Device"

ADDRESS_LABEL = "Address"

PHONE_LABEL = "Phone"

EMAIL_LABEL = "Email"


SUPPORTED_SIMILARITY_LABELS = [

    CUSTOMER_LABEL,

    COMPANY_LABEL,

    ACCOUNT_LABEL,

    DEVICE_LABEL,

    ADDRESS_LABEL,

    PHONE_LABEL,

    EMAIL_LABEL,

]


# ==========================================================
# Similarity Score Classification
# ==========================================================

VERY_HIGH_SIMILARITY = 0.95

HIGH_SIMILARITY = 0.90

MEDIUM_SIMILARITY = 0.80

LOW_SIMILARITY = 0.70


# ==========================================================
# Batch Processing
# ==========================================================

DEFAULT_BATCH_SIZE = 1000

DEFAULT_CONCURRENCY = 4


# ==========================================================
# Neo4j Property Names
# ==========================================================

SIMILARITY_CREATED_AT = "created_at"

SIMILARITY_UPDATED_AT = "updated_at"

SIMILARITY_ALGORITHM = "algorithm"