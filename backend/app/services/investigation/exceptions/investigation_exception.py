"""
==========================================================
AML Investigation Platform

Base Investigation Exception

==========================================================
"""

from __future__ import annotations


class InvestigationException(Exception):
    """
    Base exception for the Investigation module.
    """

    def __init__(
        self,
        message: str,
    ) -> None:

        super().__init__(message)

        self.message = message