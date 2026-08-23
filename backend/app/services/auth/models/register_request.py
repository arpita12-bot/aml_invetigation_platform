"""
==========================================================
AML Investigation Platform

Register Request Domain Model
==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RegisterRequest:

    username: str

    email: str

    password: str

    first_name: str

    last_name: str