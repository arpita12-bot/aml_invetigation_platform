"""
==========================================================
Validator Registry

Automatically manages all validators.

==========================================================
"""

from __future__ import annotations

from app.validators.email_validator import EmailValidator
from app.validators.phone_validator import PhoneValidator
from app.validators.date_validator import DateValidator
from app.validators.amount_validator import AmountValidator
from app.validators.currency_validator import CurrencyValidator
from app.validators.country_validator import CountryValidator

from app.validators.customer_validator import CustomerValidator
from app.validators.account_validator import AccountValidator
from app.validators.company_validator import CompanyValidator
from app.validators.transaction_validator import TransactionValidator
from app.validators.risk_validator import RiskValidator


class ValidatorRegistry:

    @staticmethod
    def get_validators():

        validators = [

            EmailValidator(),

            PhoneValidator(),

            DateValidator(),

            AmountValidator(),

            CurrencyValidator(),

            CountryValidator(),

            CustomerValidator(),

            AccountValidator(),

            CompanyValidator(),

            TransactionValidator(),

            RiskValidator(),

        ]

        validators.sort()

        return validators