"""
==========================================================
AML Investigation Platform

AML Detection Job

Responsibilities
----------------
✓ Execute AML detection rules
✓ Aggregate AML findings
✓ Build unified detection result

==========================================================
"""

from __future__ import annotations

import time

from app.models.aml_detection.aml_detection_execution_plan import (
    AMLDetectionExecutionPlan,
)

from app.models.aml_detection.aml_detection_result import (
    AMLDetectionResult,
)

from app.models.investigation.investigation_scope import (
    InvestigationScope,
)

from app.services.aml_detection.repositories.circular_payment_repository import (
    CircularPaymentRepository,
)

from app.services.aml_detection.repositories.fan_in_repository import (
    FanInRepository,
)

from app.services.aml_detection.repositories.fan_out_repository import (
    FanOutRepository,
)

from app.services.aml_detection.repositories.high_risk_country_repository import (
    HighRiskCountryRepository,
)

from app.services.aml_detection.repositories.layering_repository import (
    LayeringRepository,
)

from app.services.aml_detection.repositories.pep_detection_repository import (
    PepDetectionRepository,
)

from app.services.aml_detection.repositories.rapid_movement_repository import (
    RapidMovementRepository,
)

from app.services.aml_detection.repositories.sanction_detection_repository import (
    SanctionDetectionRepository,
)

from app.services.aml_detection.repositories.shared_device_repository import (
    SharedDeviceRepository,
)

from app.services.aml_detection.repositories.shared_ip_repository import (
    SharedIPRepository,
)

from app.services.aml_detection.repositories.structuring_repository import (
    StructuringRepository,
)


class AMLDetectionJob:
    """
    Executes all AML detection rules for a single investigation.
    """

    def __init__(
        self,
        layering_repository: LayeringRepository,
        structuring_repository: StructuringRepository,
        circular_payment_repository: CircularPaymentRepository,
        shared_device_repository: SharedDeviceRepository,
        shared_ip_repository: SharedIPRepository,
        fan_in_repository: FanInRepository,
        fan_out_repository: FanOutRepository,
        rapid_movement_repository: RapidMovementRepository,
        high_risk_country_repository: HighRiskCountryRepository,
        pep_detection_repository: PepDetectionRepository,
        sanction_detection_repository: SanctionDetectionRepository,
    ):

        self._layering = layering_repository

        self._structuring = structuring_repository

        self._circular = circular_payment_repository

        self._shared_device = shared_device_repository

        self._shared_ip = shared_ip_repository

        self._fan_in = fan_in_repository

        self._fan_out = fan_out_repository

        self._rapid = rapid_movement_repository

        self._country = high_risk_country_repository

        self._pep = pep_detection_repository

        self._sanction = sanction_detection_repository

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def execute(
        self,
        scope: InvestigationScope,
        plan: AMLDetectionExecutionPlan | None = None,
    ) -> AMLDetectionResult:

        if plan is None:

            plan = AMLDetectionExecutionPlan()

        start = time.perf_counter()

        result = AMLDetectionResult()

        self._execute_rule(
            enabled=plan.run_layering,
            repository=self._layering,
            scope=scope,
            result=result,
            rule_name="Layering",
        )

        self._execute_rule(
            enabled=plan.run_structuring,
            repository=self._structuring,
            scope=scope,
            result=result,
            rule_name="Structuring",
        )

        self._execute_rule(
            enabled=plan.run_circular_payments,
            repository=self._circular,
            scope=scope,
            result=result,
            rule_name="Circular Payments",
        )

        self._execute_rule(
            enabled=plan.run_shared_devices,
            repository=self._shared_device,
            scope=scope,
            result=result,
            rule_name="Shared Device",
        )

        self._execute_rule(
            enabled=plan.run_shared_ips,
            repository=self._shared_ip,
            scope=scope,
            result=result,
            rule_name="Shared IP",
        )

        self._execute_rule(
            enabled=plan.run_fan_in,
            repository=self._fan_in,
            scope=scope,
            result=result,
            rule_name="Fan-In",
        )

        self._execute_rule(
            enabled=plan.run_fan_out,
            repository=self._fan_out,
            scope=scope,
            result=result,
            rule_name="Fan-Out",
        )

        self._execute_rule(
            enabled=plan.run_rapid_movement,
            repository=self._rapid,
            scope=scope,
            result=result,
            rule_name="Rapid Movement",
        )

        self._execute_rule(
            enabled=plan.run_high_risk_country,
            repository=self._country,
            scope=scope,
            result=result,
            rule_name="High Risk Country",
        )

        self._execute_rule(
            enabled=plan.run_pep_detection,
            repository=self._pep,
            scope=scope,
            result=result,
            rule_name="PEP",
        )

        self._execute_rule(
            enabled=plan.run_sanction_detection,
            repository=self._sanction,
            scope=scope,
            result=result,
            rule_name="Sanctions",
        )

        result.execution_time_seconds = round(
            time.perf_counter() - start,
            3,
        )

        result.successful = len(result.errors) == 0

        return result

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------

    def _execute_rule(
        self,
        *,
        enabled: bool,
        repository,
        scope: InvestigationScope,
        result: AMLDetectionResult,
        rule_name: str,
    ) -> None:

        if not enabled:
            return

        try:

            findings = repository.detect(scope)

            result.findings.extend(findings)

        except Exception as exc:

            result.errors.append(
                f"{rule_name}: {type(exc).__name__}: {exc}"
            )