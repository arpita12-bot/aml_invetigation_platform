"""
==========================================================

AML Investigation Platform

Enterprise Blocking Utilities

Responsibilities
----------------

✓ Country normalization
✓ Phone normalization
✓ Email normalization
✓ Postal normalization
✓ Composite blocking keys
✓ Blocking helper utilities

==========================================================
"""

from __future__ import annotations

import re

from typing import Optional
from typing import List

from app.utils.phonetic_utils import PhoneticUtils


class BlockingUtils:

    """
    Enterprise Blocking Utilities
    """

    # -----------------------------------------------------
    # Country
    # -----------------------------------------------------

    @staticmethod
    def normalize_country(
        country: Optional[str]
    ) -> str:

        if not country:
            return ""

        country = country.upper().strip()

        country = re.sub(r"\s+", " ", country)

        return country

    # -----------------------------------------------------
    # City
    # -----------------------------------------------------

    @staticmethod
    def normalize_city(
        city: Optional[str]
    ) -> str:

        if not city:
            return ""

        city = city.lower().strip()

        city = re.sub(r"\s+", " ", city)

        return city.title()

    # -----------------------------------------------------
    # Postal Code
    # -----------------------------------------------------

    @staticmethod
    def normalize_postal(
        postal_code: Optional[str]
    ) -> str:

        if not postal_code:
            return ""

        postal_code = str(postal_code)

        postal_code = postal_code.strip()

        postal_code = postal_code.replace(" ", "")

        postal_code = postal_code.upper()

        return postal_code

    # -----------------------------------------------------
    # Phone
    # -----------------------------------------------------

    @staticmethod
    def normalize_phone(
        phone: Optional[str]
    ) -> str:

        if not phone:
            return ""

        digits = re.sub(r"\D", "", str(phone))

        return digits

    # -----------------------------------------------------
    # Phone Prefix
    # -----------------------------------------------------

    @staticmethod
    def phone_prefix(
        phone: Optional[str],
        length: int = 5
    ) -> str:

        digits = BlockingUtils.normalize_phone(phone)

        return digits[:length]

    # -----------------------------------------------------
    # Email
    # -----------------------------------------------------

    @staticmethod
    def normalize_email(
        email: Optional[str]
    ) -> str:

        if not email:
            return ""

        return email.strip().lower()

    # -----------------------------------------------------
    # Email Domain
    # -----------------------------------------------------

    @staticmethod
    def email_domain(
        email: Optional[str]
    ) -> str:

        email = BlockingUtils.normalize_email(email)

        if "@" not in email:

            return ""

        return email.split("@")[1]
    
        # -----------------------------------------------------
    # Company
    # -----------------------------------------------------

    @staticmethod
    def normalize_company(
        company: Optional[str]
    ) -> str:
        """
        Normalize company names.

        Example
        -------
        IBM INDIA PVT. LTD.

        →

        Ibm India Pvt Ltd
        """

        if not company:
            return ""

        company = company.strip().lower()

        company = re.sub(r"[^\w\s]", " ", company)

        company = re.sub(r"\s+", " ", company)

        return company.title()

    # -----------------------------------------------------
    # Nationality
    # -----------------------------------------------------

    @staticmethod
    def normalize_nationality(
        nationality: Optional[str]
    ) -> str:

        if not nationality:
            return ""

        nationality = nationality.strip().upper()

        nationality = re.sub(r"\s+", " ", nationality)

        return nationality

    # -----------------------------------------------------
    # Customer Type
    # -----------------------------------------------------

    @staticmethod
    def normalize_customer_type(
        customer_type: Optional[str]
    ) -> str:

        if not customer_type:
            return ""

        return customer_type.strip().upper()

    # -----------------------------------------------------
    # Risk Level
    # -----------------------------------------------------

    @staticmethod
    def normalize_risk_level(
        risk_level: Optional[str]
    ) -> str:

        if not risk_level:
            return ""

        value = risk_level.strip().upper()

        mapping = {
            "H": "HIGH",
            "M": "MEDIUM",
            "L": "LOW"
        }

        return mapping.get(value, value)

    # -----------------------------------------------------
    # DOB Year
    # -----------------------------------------------------

    @staticmethod
    def extract_birth_year(
        dob
    ) -> str:
        """
        Accepts either a date, datetime,
        or ISO date string.
        """

        if dob is None:
            return ""

        try:

            if hasattr(dob, "year"):
                return str(dob.year)

            return str(dob)[:4]

        except Exception:

            return ""

    # -----------------------------------------------------
    # Country Key
    # -----------------------------------------------------

    @staticmethod
    def build_country_key(
        country: Optional[str]
    ) -> str:

        country = BlockingUtils.normalize_country(country)

        if not country:
            return ""

        return country[:3]

    # -----------------------------------------------------
    # Phone Key
    # -----------------------------------------------------

    @staticmethod
    def build_phone_key(
        phone: Optional[str]
    ) -> str:

        return BlockingUtils.phone_prefix(phone)

    # -----------------------------------------------------
    # Email Key
    # -----------------------------------------------------

    @staticmethod
    def build_email_key(
        email: Optional[str]
    ) -> str:

        return BlockingUtils.email_domain(email)

    # -----------------------------------------------------
    # Company Key
    # -----------------------------------------------------

    @staticmethod
    def build_company_key(
        company: Optional[str]
    ) -> str:

        company = BlockingUtils.normalize_company(company)

        if not company:
            return ""

        words = company.split()

        return "_".join(words[:2])

    # -----------------------------------------------------
    # Name Key
    # -----------------------------------------------------

    @staticmethod
    def build_name_key(
        name: Optional[str]
    ) -> str:
        """
        Uses the surname Soundex generated
        by PhoneticUtils.
        """

        return PhoneticUtils.phonetic_block_key(name)

    # -----------------------------------------------------
    # DOB Key
    # -----------------------------------------------------

    @staticmethod
    def build_dob_key(
        dob
    ) -> str:

        return BlockingUtils.extract_birth_year(dob)
    
        # -----------------------------------------------------
    # Company
    # -----------------------------------------------------

    @staticmethod
    def normalize_company(
        company: Optional[str]
    ) -> str:
        """
        Normalize company names.

        Example
        -------
        IBM INDIA PVT. LTD.

        →

        Ibm India Pvt Ltd
        """

        if not company:
            return ""

        company = company.strip().lower()

        company = re.sub(r"[^\w\s]", " ", company)

        company = re.sub(r"\s+", " ", company)

        return company.title()

    # -----------------------------------------------------
    # Nationality
    # -----------------------------------------------------

    @staticmethod
    def normalize_nationality(
        nationality: Optional[str]
    ) -> str:

        if not nationality:
            return ""

        nationality = nationality.strip().upper()

        nationality = re.sub(r"\s+", " ", nationality)

        return nationality

    # -----------------------------------------------------
    # Customer Type
    # -----------------------------------------------------

    @staticmethod
    def normalize_customer_type(
        customer_type: Optional[str]
    ) -> str:

        if not customer_type:
            return ""

        return customer_type.strip().upper()

    # -----------------------------------------------------
    # Risk Level
    # -----------------------------------------------------

    @staticmethod
    def normalize_risk_level(
        risk_level: Optional[str]
    ) -> str:

        if not risk_level:
            return ""

        value = risk_level.strip().upper()

        mapping = {
            "H": "HIGH",
            "M": "MEDIUM",
            "L": "LOW"
        }

        return mapping.get(value, value)

    # -----------------------------------------------------
    # DOB Year
    # -----------------------------------------------------

    @staticmethod
    def extract_birth_year(
        dob
    ) -> str:
        """
        Accepts either a date, datetime,
        or ISO date string.
        """

        if dob is None:
            return ""

        try:

            if hasattr(dob, "year"):
                return str(dob.year)

            return str(dob)[:4]

        except Exception:

            return ""

    # -----------------------------------------------------
    # Country Key
    # -----------------------------------------------------

    @staticmethod
    def build_country_key(
        country: Optional[str]
    ) -> str:

        country = BlockingUtils.normalize_country(country)

        if not country:
            return ""

        return country[:3]

    # -----------------------------------------------------
    # Phone Key
    # -----------------------------------------------------

    @staticmethod
    def build_phone_key(
        phone: Optional[str]
    ) -> str:

        return BlockingUtils.phone_prefix(phone)

    # -----------------------------------------------------
    # Email Key
    # -----------------------------------------------------

    @staticmethod
    def build_email_key(
        email: Optional[str]
    ) -> str:

        return BlockingUtils.email_domain(email)

    # -----------------------------------------------------
    # Company Key
    # -----------------------------------------------------

    @staticmethod
    def build_company_key(
        company: Optional[str]
    ) -> str:

        company = BlockingUtils.normalize_company(company)

        if not company:
            return ""

        words = company.split()

        return "_".join(words[:2])

    # -----------------------------------------------------
    # Name Key
    # -----------------------------------------------------

    @staticmethod
    def build_name_key(
        name: Optional[str]
    ) -> str:
        """
        Uses the surname Soundex generated
        by PhoneticUtils.
        """

        return PhoneticUtils.phonetic_block_key(name)

    # -----------------------------------------------------
    # DOB Key
    # -----------------------------------------------------

    @staticmethod
    def build_dob_key(
        dob
    ) -> str:

        return BlockingUtils.extract_birth_year(dob)