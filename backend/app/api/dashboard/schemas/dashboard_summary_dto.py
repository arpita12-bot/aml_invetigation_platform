"""
==========================================================
AML Investigation Platform

Dashboard DTOs
==========================================================
"""

from pydantic import BaseModel


class DashboardSummaryDTO(BaseModel):

    customers: int

    accounts: int

    transactions: int

    companies: int

    pep: int

    sanctions: int

    investigations: int

    uploaded_datasets: int

    high_risk_customers: int