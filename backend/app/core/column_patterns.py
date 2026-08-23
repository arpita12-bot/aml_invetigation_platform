"""
==========================================================
AML Investigation Platform

Column Detection Patterns

Responsibilities
----------------
✓ Centralized AML column aliases
✓ Dynamic dataset support
✓ Easy customization
✓ Validator configuration

==========================================================
"""

# ==========================================================
# Email
# ==========================================================

EMAIL_PATTERNS = [
    "email",
    "email_id",
    "customer_email",
    "mail",
    "e_mail",
]

# ==========================================================
# Phone
# ==========================================================

PHONE_PATTERNS = [
    "phone",
    "phone_number",
    "mobile",
    "mobile_number",
    "telephone",
    "contact_number",
]

# ==========================================================
# Date
# ==========================================================

DATE_PATTERNS = [
    "date",
    "dob",
    "birth_date",
    "transaction_date",
    "created_date",
    "updated_date",
    "opened_date",
    "closed_date",
]

# ==========================================================
# Amount
# ==========================================================

AMOUNT_PATTERNS = [
    "amount",
    "transaction_amount",
    "payment_amount",
    "balance",
    "salary",
    "income",
    "credit",
    "debit",
    "value",
]

# ==========================================================
# Currency
# ==========================================================

CURRENCY_PATTERNS = [
    "currency",
    "currency_code",
]

# ==========================================================
# Country
# ==========================================================

COUNTRY_PATTERNS = [
    "country",
    "country_code",
    "nationality",
    "citizenship",
]

# ==========================================================
# Customer
# ==========================================================

CUSTOMER_PATTERNS = [
    "customer",
    "customer_id",
    "client",
    "client_id",
]

# ==========================================================
# Account
# ==========================================================

ACCOUNT_PATTERNS = [
    "account",
    "account_number",
    "account_no",
    "iban",
    "swift",
    "bic",
]

# ==========================================================
# Company
# ==========================================================

COMPANY_PATTERNS = [
    "company",
    "company_name",
    "business_name",
    "registration_number",
    "registration_no",
    "tax_id",
]

# ==========================================================
# Transaction
# ==========================================================

TRANSACTION_PATTERNS = [
    "transaction",
    "transaction_id",
    "txn_id",
    "reference_number",
]

# ==========================================================
# Risk
# ==========================================================

RISK_PATTERNS = [
    "risk",
    "risk_score",
    "risk_level",
]


SEMANTIC_PATTERNS = {

    # Customer

    "CUSTOMER_ID": [
        "customer_id",
        "cust_id",
        "customer",
        "cust_no",
        "customer_number",
        "client_id",
        "party_id",
    ],

    "ACCOUNT_ID": [
        "account_id",
        "account",
        "acct",
        "account_number",
        "iban",
    ],

    "TRANSACTION_ID": [
        "transaction_id",
        "txn_id",
        "transaction",
        "trx_id",
    ],

    "TRANSACTION_AMOUNT": [
        "amount",
        "amt",
        "transaction_amount",
        "payment_amount",
        "value",
    ],

    "EMAIL": [
        "email",
        "mail",
        "email_address",
    ],

    "PHONE": [
        "phone",
        "mobile",
        "telephone",
        "contact_number",
    ],

    "COUNTRY": [
        "country",
        "country_code",
    ],

    "CITY": [
        "city",
    ],

    "ADDRESS": [
        "address",
        "street",
    ],

    "DOB": [
        "dob",
        "birth_date",
        "date_of_birth",
    ],

    "PEP_FLAG": [
        "pep",
        "pep_flag",
    ],

    "SANCTION_FLAG": [
        "sanction",
        "sanction_flag",
    ],

    "WATCHLIST_FLAG": [
        "watchlist",
        "watchlist_flag",
    ],

    "RISK_SCORE": [
        "risk_score",
        "score",
    ],

    "DEVICE_ID": [
        "device",
        "device_id",
    ],

    "IP_ADDRESS": [
        "ip",
        "ip_address",
    ],

    "COMPANY_ID": [
        "company",
        "company_id",
        "organization",
    ],

    "SWIFT_CODE": [
        "swift",
        "swift_code",
        "bic",
    ],

    "CRYPTO_WALLET": [
        "wallet",
        "wallet_address",
        "crypto_wallet",
    ],
}