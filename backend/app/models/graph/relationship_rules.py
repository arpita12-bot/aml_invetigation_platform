"""
==========================================================
Relationship Rules

Defines business relationships used for graph generation.

==========================================================
"""


class RelationshipRules:

    """
    Business relationship definitions.
    """

    RULES = {

        (
            "CUSTOMER_ID",
            "ACCOUNT_ID",
        ): "OWNS",

        (
            "ACCOUNT_ID",
            "TRANSACTION_ID",
        ): "PERFORMS",

        (
            "CUSTOMER_ID",
            "PHONE",
        ): "USES",

        (
            "CUSTOMER_ID",
            "EMAIL",
        ): "USES",

        (
            "CUSTOMER_ID",
            "DEVICE_ID",
        ): "USES",

        (
            "CUSTOMER_ID",
            "IP_ADDRESS",
        ): "CONNECTS_FROM",

        (
            "CUSTOMER_ID",
            "COMPANY_ID",
        ): "DIRECTOR_OF",

        (
            "COMPANY_ID",
            "BENEFICIAL_OWNER",
        ): "OWNED_BY",

        (
            "CUSTOMER_ID",
            "PEP_ID",
        ): "MATCHES",

        (
            "CUSTOMER_ID",
            "SANCTION_ID",
        ): "MATCHES",

    }