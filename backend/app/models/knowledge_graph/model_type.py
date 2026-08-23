"""
==========================================================
AML Investigation Platform

Knowledge Graph Embedding Models

==========================================================
"""

from __future__ import annotations

from enum import Enum


class ModelType(str, Enum):
    """
    Supported Knowledge Graph Embedding models.
    """

    TRANSE = "TransE"

    ROTATE = "RotatE"

    COMPLEX = "ComplEx"

    DISTMULT = "DistMult"

    RESCAL = "RESCAL"

    CONVE = "ConvE"