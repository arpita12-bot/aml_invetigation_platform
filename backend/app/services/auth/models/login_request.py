"""
==========================================================
AML Investigation Platform

Login Request Domain Model
==========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class LoginRequest:

    username: str

    password: str