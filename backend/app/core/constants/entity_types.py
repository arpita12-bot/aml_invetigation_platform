"""
==========================================================
AML Investigation Platform

Entity Types

Responsibilities
----------------
✓ Define supported AML entity types
✓ Provide a single source of truth
✓ Eliminate hard-coded string literals

==========================================================
"""

from __future__ import annotations

# Core entities
CUSTOMER = "CUSTOMER"
ACCOUNT = "ACCOUNT"
COMPANY = "COMPANY"
TRANSACTION = "TRANSACTION"

# Contact entities
DEVICE = "DEVICE"
PHONE = "PHONE"
EMAIL = "EMAIL"
IP_ADDRESS = "IP_ADDRESS"

# Compliance entities
PEP = "PEP"
SANCTION = "SANCTION"
WATCHLIST = "WATCHLIST"
ADVERSE_NEWS = "ADVERSE_NEWS"

SUPPORTED_ENTITY_TYPES = frozenset(
    {
        CUSTOMER,
        ACCOUNT,
        COMPANY,
        TRANSACTION,
        DEVICE,
        PHONE,
        EMAIL,
        IP_ADDRESS,
        PEP,
        SANCTION,
        WATCHLIST,
        ADVERSE_NEWS,
    }
)

__all__ = [
    "CUSTOMER",
    "ACCOUNT",
    "COMPANY",
    "TRANSACTION",
    "DEVICE",
    "PHONE",
    "EMAIL",
    "IP_ADDRESS",
    "PEP",
    "SANCTION",
    "WATCHLIST",
    "ADVERSE_NEWS",
    "SUPPORTED_ENTITY_TYPES",
]