"""
==========================================================
AML Investigation Platform

Shell Candidate DTO
==========================================================
"""

from pydantic import BaseModel, Field


class ShellCandidateDTO(BaseModel):
    company_id: str

    company_name: str

    suspicion_score: float

    risk_level: str

    explanation: str