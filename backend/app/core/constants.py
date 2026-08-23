"""
==========================================================
AML Investigation Platform

Application Constants

Responsibilities
----------------
✓ PostgreSQL Reserved Keywords
✓ Upload Status Constants
✓ Validation Status Constants
✓ Processing Status Constants
✓ Graph Status Constants

==========================================================
"""

from enum import Enum

# ==========================================================
# PostgreSQL Reserved Keywords
# ==========================================================

POSTGRES_RESERVED_WORDS = {
    "all",
    "analyse",
    "analyze",
    "and",
    "any",
    "array",
    "as",
    "asc",
    "asymmetric",
    "authorization",
    "between",
    "binary",
    "both",
    "case",
    "cast",
    "check",
    "collate",
    "column",
    "constraint",
    "create",
    "cross",
    "current_catalog",
    "current_date",
    "current_role",
    "current_schema",
    "current_time",
    "current_timestamp",
    "current_user",
    "default",
    "deferrable",
    "desc",
    "distinct",
    "do",
    "else",
    "end",
    "except",
    "exists",
    "false",
    "fetch",
    "for",
    "foreign",
    "from",
    "full",
    "grant",
    "group",
    "having",
    "in",
    "initially",
    "inner",
    "intersect",
    "into",
    "is",
    "join",
    "leading",
    "left",
    "like",
    "limit",
    "localtime",
    "localtimestamp",
    "natural",
    "not",
    "null",
    "offset",
    "on",
    "only",
    "or",
    "order",
    "outer",
    "placing",
    "primary",
    "references",
    "returning",
    "right",
    "select",
    "session_user",
    "some",
    "symmetric",
    "table",
    "then",
    "to",
    "trailing",
    "true",
    "union",
    "unique",
    "user",
    "using",
    "variadic",
    "verbose",
    "when",
    "where",
    "window",
    "with",
}


# ==========================================================
# Upload Status
# ==========================================================

class UploadStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DUPLICATE = "DUPLICATE"


# ==========================================================
# Validation Status
# ==========================================================

class ValidationStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


# ==========================================================
# Processing Status
# ==========================================================

class ProcessingStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ==========================================================
# Graph Status
# ==========================================================

class GraphStatus(str, Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    FAILED = "FAILED"


# ==========================================================
# ML Status
# ==========================================================

class MLStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"