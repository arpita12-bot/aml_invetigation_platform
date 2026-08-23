"""
==========================================================
AML Investigation Platform

Shell Pattern Result

Represents graph-derived shell company indicators.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ShellPatternResult:

    shared_directors: int = 0

    shared_addresses: int = 0

    shared_phone_numbers: int = 0

    shared_devices: int = 0

    shared_bank_accounts: int = 0

    ownership_depth: int = 0

    circular_transaction_count: int = 0

    high_risk_neighbors: int = 0

    shell_pattern_score: float = 0.0

    def to_dict(self) -> dict:

        return {

            "shared_directors": self.shared_directors,

            "shared_addresses": self.shared_addresses,

            "shared_phone_numbers": self.shared_phone_numbers,

            "shared_devices": self.shared_devices,

            "shared_bank_accounts": self.shared_bank_accounts,

            "ownership_depth": self.ownership_depth,

            "circular_transaction_count":
                self.circular_transaction_count,

            "high_risk_neighbors":
                self.high_risk_neighbors,

            "shell_pattern_score":
                self.shell_pattern_score,
        }