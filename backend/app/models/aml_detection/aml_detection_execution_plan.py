"""
==========================================================
AML Investigation Platform

AML Detection Execution Plan

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AMLDetectionExecutionPlan:

    run_layering: bool = True

    run_structuring: bool = True

    run_circular_payments: bool = True

    run_shared_devices: bool = True

    run_shared_ips: bool = True

    run_fan_in: bool = True

    run_fan_out: bool = True

    run_rapid_movement: bool = True

    run_high_risk_country: bool = True

    run_pep_detection: bool = True

    run_sanction_detection: bool = True