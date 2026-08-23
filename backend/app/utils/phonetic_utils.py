"""
==========================================================
AML Investigation Platform

Enterprise Phonetic Utilities

Responsibilities
----------------
✓ Unicode normalization
✓ Accent removal
✓ Name cleaning
✓ Soundex encoding
✓ Phonetic comparison
✓ Initial extraction
✓ Tokenization
✓ Name normalization

Author : AML Platform
==========================================================
"""

from __future__ import annotations

import re
import unicodedata
from typing import List, Optional

try:
    from metaphone import doublemetaphone

    METAPHONE_AVAILABLE = True
except ImportError:
    METAPHONE_AVAILABLE = False


class PhoneticUtils:
    """
    Enterprise phonetic helper methods.
    """

    # ---------------------------------------------------------
    # Unicode
    # ---------------------------------------------------------

    @staticmethod
    def remove_accents(text: Optional[str]) -> str:
        """
        José
            ->
        Jose
        """

        if not text:
            return ""

        normalized = unicodedata.normalize("NFKD", text)

        return "".join(
            c
            for c in normalized
            if not unicodedata.combining(c)
        )

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------

    @staticmethod
    def normalize_name(name: Optional[str]) -> str:
        """
        Normalize names.

        Example

        JOHN   SMITH

        →

        john smith
        """

        if not name:
            return ""

        name = PhoneticUtils.remove_accents(name)

        name = name.lower()

        name = re.sub(r"[^a-z0-9 ]", " ", name)

        name = re.sub(r"\s+", " ", name)

        return name.strip()

    # ---------------------------------------------------------
    # Tokenization
    # ---------------------------------------------------------

    @staticmethod
    def tokenize(name: Optional[str]) -> List[str]:

        normalized = PhoneticUtils.normalize_name(name)

        if not normalized:
            return []

        return normalized.split()

    # ---------------------------------------------------------
    # Initials
    # ---------------------------------------------------------

    @staticmethod
    def initials(name: Optional[str]) -> str:
        """
        John William Smith

        ->

        JWS
        """

        tokens = PhoneticUtils.tokenize(name)

        if not tokens:
            return ""

        return "".join(token[0].upper() for token in tokens)

    # ---------------------------------------------------------
    # First Name
    # ---------------------------------------------------------

    @staticmethod
    def first_name(name: Optional[str]) -> str:

        tokens = PhoneticUtils.tokenize(name)

        if not tokens:
            return ""

        return tokens[0]

    # ---------------------------------------------------------
    # Last Name
    # ---------------------------------------------------------

    @staticmethod
    def last_name(name: Optional[str]) -> str:

        tokens = PhoneticUtils.tokenize(name)

        if not tokens:
            return ""

        return tokens[-1]
    
    # ---------------------------------------------------------
    # Soundex Mapping
    # ---------------------------------------------------------

    _SOUNDEX_MAPPING = {
        "B": "1", "F": "1", "P": "1", "V": "1",
        "C": "2", "G": "2", "J": "2", "K": "2",
        "Q": "2", "S": "2", "X": "2", "Z": "2",
        "D": "3", "T": "3",
        "L": "4",
        "M": "5", "N": "5",
        "R": "6",
    }

    # ---------------------------------------------------------
    # Soundex
    # ---------------------------------------------------------

    @staticmethod
    def soundex(name: Optional[str]) -> str:
        """
        Generate the standard Soundex code.

        Examples
        --------
        Robert  -> R163
        Rupert  -> R163
        Rubin   -> R150
        Ashcraft -> A261
        """

        if not name:
            return ""

        cleaned = PhoneticUtils.normalize_name(name).replace(" ", "").upper()

        if not cleaned:
            return ""

        first_letter = cleaned[0]

        encoded = []

        previous = PhoneticUtils._SOUNDEX_MAPPING.get(first_letter, "")

        for char in cleaned[1:]:

            code = PhoneticUtils._SOUNDEX_MAPPING.get(char, "")

            if not code:
                previous = ""
                continue

            if code != previous:
                encoded.append(code)

            previous = code

        soundex_code = first_letter + "".join(encoded)

        soundex_code = soundex_code[:4]

        return soundex_code.ljust(4, "0")

    # ---------------------------------------------------------
    # Batch Soundex
    # ---------------------------------------------------------

    @staticmethod
    def batch_soundex(names: List[str]) -> List[str]:
        """
        Generate Soundex codes for multiple names.
        """

        return [
            PhoneticUtils.soundex(name)
            for name in names
        ]

    # ---------------------------------------------------------
    # Soundex Comparison
    # ---------------------------------------------------------

    @staticmethod
    def soundex_match(
        left: Optional[str],
        right: Optional[str],
    ) -> bool:
        """
        Compare two names using Soundex.
        """

        if not left or not right:
            return False

        return (
            PhoneticUtils.soundex(left)
            == PhoneticUtils.soundex(right)
        )

    # ---------------------------------------------------------
    # Batch Comparison
    # ---------------------------------------------------------

    @staticmethod
    def compare_against_list(
        target: str,
        candidates: List[str],
    ) -> List[str]:
        """
        Return candidate names that share the same
        Soundex code as the target.
        """

        target_code = PhoneticUtils.soundex(target)

        matches = []

        for candidate in candidates:

            if PhoneticUtils.soundex(candidate) == target_code:
                matches.append(candidate)

        return matches

    # ---------------------------------------------------------
    # Soundex Dictionary
    # ---------------------------------------------------------

    @staticmethod
    def build_soundex_index(
        names: List[str],
    ) -> dict[str, List[str]]:
        """
        Build an index of Soundex code -> names.

        Example
        -------
        {
            "R163": ["Robert", "Rupert"],
            "S530": ["Smith", "Smyth"]
        }
        """

        index: dict[str, List[str]] = {}

        for name in names:

            code = PhoneticUtils.soundex(name)

            index.setdefault(code, []).append(name)

        return index

    # ---------------------------------------------------------
    # Blocking Key
    # ---------------------------------------------------------

    @staticmethod
    def phonetic_block_key(name: Optional[str]) -> str:
        """
        Generate a normalized blocking key.

        Example
        -------
        John Smith

        ->
        S530
        """

        surname = PhoneticUtils.last_name(name)

        if not surname:
            surname = PhoneticUtils.normalize_name(name)

        return PhoneticUtils.soundex(surname)
    
        # ---------------------------------------------------------
    # Double Metaphone
    # ---------------------------------------------------------

    @staticmethod
    def metaphone(name: Optional[str]) -> tuple[str, str]:
        """
        Generate Double Metaphone codes.

        Returns
        -------
        (primary, secondary)

        If the metaphone package is unavailable,
        Soundex is used as a fallback.
        """

        if not name:
            return "", ""

        normalized = PhoneticUtils.normalize_name(name)

        if not normalized:
            return "", ""

        if METAPHONE_AVAILABLE:
            primary, secondary = doublemetaphone(normalized)
            return primary or "", secondary or ""

        code = PhoneticUtils.soundex(normalized)

        return code, ""

    # ---------------------------------------------------------
    # Primary Metaphone
    # ---------------------------------------------------------

    @staticmethod
    def primary_metaphone(name: Optional[str]) -> str:

        return PhoneticUtils.metaphone(name)[0]

    # ---------------------------------------------------------
    # Secondary Metaphone
    # ---------------------------------------------------------

    @staticmethod
    def secondary_metaphone(name: Optional[str]) -> str:

        return PhoneticUtils.metaphone(name)[1]

    # ---------------------------------------------------------
    # Metaphone Match
    # ---------------------------------------------------------

    @staticmethod
    def metaphone_match(
        left: Optional[str],
        right: Optional[str],
    ) -> bool:
        """
        Compare names using Double Metaphone.
        """

        if not left or not right:
            return False

        left_codes = set(
            code
            for code in PhoneticUtils.metaphone(left)
            if code
        )

        right_codes = set(
            code
            for code in PhoneticUtils.metaphone(right)
            if code
        )

        return len(left_codes.intersection(right_codes)) > 0

    # ---------------------------------------------------------
    # Initial + Surname Fingerprint
    # ---------------------------------------------------------

    @staticmethod
    def name_fingerprint(name: Optional[str]) -> str:
        """
        Example

        John William Smith

        →

        J_S530
        """

        if not name:
            return ""

        first = PhoneticUtils.first_name(name)
        last = PhoneticUtils.last_name(name)

        if not first:
            return ""

        initial = first[0].upper()

        soundex = PhoneticUtils.soundex(last)

        return f"{initial}_{soundex}"

    # ---------------------------------------------------------
    # Canonical Name
    # ---------------------------------------------------------

    @staticmethod
    def canonical_name(name: Optional[str]) -> str:
        """
        Convert a name into a canonical representation
        suitable for duplicate detection.

        Example

        José A. Smith

        →

        jose smith
        """

        tokens = PhoneticUtils.tokenize(name)

        if not tokens:
            return ""

        filtered = [
            token
            for token in tokens
            if len(token) > 1
        ]

        return " ".join(filtered)

    # ---------------------------------------------------------
    # Canonical Phonetic Key
    # ---------------------------------------------------------

    @staticmethod
    def canonical_phonetic_key(
        name: Optional[str],
    ) -> str:
        """
        Example

        John William Smith

        →

        JOHN_S530
        """

        if not name:
            return ""

        first = PhoneticUtils.first_name(name).upper()

        surname = PhoneticUtils.last_name(name)

        code = PhoneticUtils.soundex(surname)

        return f"{first}_{code}"

    # ---------------------------------------------------------
    # Phonetic Similarity
    # ---------------------------------------------------------

    @staticmethod
    def phonetic_similarity(
        left: Optional[str],
        right: Optional[str],
    ) -> float:
        """
        Returns

        1.0  = identical

        0.5  = partial phonetic match

        0.0  = different
        """

        if not left or not right:
            return 0.0

        if (
            PhoneticUtils.soundex(left)
            ==
            PhoneticUtils.soundex(right)
        ):
            return 1.0

        if PhoneticUtils.metaphone_match(left, right):
            return 0.75

        left_initial = PhoneticUtils.initials(left)
        right_initial = PhoneticUtils.initials(right)

        if left_initial == right_initial:
            return 0.50

        return 0.0

    # ---------------------------------------------------------
    # Phonetic Index
    # ---------------------------------------------------------

    @staticmethod
    def build_phonetic_index(
        names: List[str],
    ) -> dict[str, List[str]]:
        """
        Build an index using canonical phonetic keys.
        """

        index: dict[str, List[str]] = {}

        for name in names:

            key = PhoneticUtils.canonical_phonetic_key(name)

            index.setdefault(key, []).append(name)

        return index

    # ---------------------------------------------------------
    # Best Phonetic Candidates
    # ---------------------------------------------------------

    @staticmethod
    def phonetic_candidates(
        target: str,
        names: List[str],
        threshold: float = 0.75,
    ) -> List[str]:
        """
        Return names whose phonetic similarity
        exceeds the threshold.
        """

        matches = []

        for candidate in names:

            score = PhoneticUtils.phonetic_similarity(
                target,
                candidate,
            )

            if score >= threshold:
                matches.append(candidate)

        return matches
    
    # ---------------------------------------------------------
    # Double Metaphone
    # ---------------------------------------------------------

    @staticmethod
    def metaphone(name: Optional[str]) -> tuple[str, str]:
        """
        Generate Double Metaphone codes.

        Returns
        -------
        (primary, secondary)

        If the metaphone package is unavailable,
        Soundex is used as a fallback.
        """

        if not name:
            return "", ""

        normalized = PhoneticUtils.normalize_name(name)

        if not normalized:
            return "", ""

        if METAPHONE_AVAILABLE:
            primary, secondary = doublemetaphone(normalized)
            return primary or "", secondary or ""

        code = PhoneticUtils.soundex(normalized)

        return code, ""

    # ---------------------------------------------------------
    # Primary Metaphone
    # ---------------------------------------------------------

    @staticmethod
    def primary_metaphone(name: Optional[str]) -> str:

        return PhoneticUtils.metaphone(name)[0]

    # ---------------------------------------------------------
    # Secondary Metaphone
    # ---------------------------------------------------------

    @staticmethod
    def secondary_metaphone(name: Optional[str]) -> str:

        return PhoneticUtils.metaphone(name)[1]

    # ---------------------------------------------------------
    # Metaphone Match
    # ---------------------------------------------------------

    @staticmethod
    def metaphone_match(
        left: Optional[str],
        right: Optional[str],
    ) -> bool:
        """
        Compare names using Double Metaphone.
        """

        if not left or not right:
            return False

        left_codes = set(
            code
            for code in PhoneticUtils.metaphone(left)
            if code
        )

        right_codes = set(
            code
            for code in PhoneticUtils.metaphone(right)
            if code
        )

        return len(left_codes.intersection(right_codes)) > 0

    # ---------------------------------------------------------
    # Initial + Surname Fingerprint
    # ---------------------------------------------------------

    @staticmethod
    def name_fingerprint(name: Optional[str]) -> str:
        """
        Example

        John William Smith

        →

        J_S530
        """

        if not name:
            return ""

        first = PhoneticUtils.first_name(name)
        last = PhoneticUtils.last_name(name)

        if not first:
            return ""

        initial = first[0].upper()

        soundex = PhoneticUtils.soundex(last)

        return f"{initial}_{soundex}"

    # ---------------------------------------------------------
    # Canonical Name
    # ---------------------------------------------------------

    @staticmethod
    def canonical_name(name: Optional[str]) -> str:
        """
        Convert a name into a canonical representation
        suitable for duplicate detection.

        Example

        José A. Smith

        →

        jose smith
        """

        tokens = PhoneticUtils.tokenize(name)

        if not tokens:
            return ""

        filtered = [
            token
            for token in tokens
            if len(token) > 1
        ]

        return " ".join(filtered)

    # ---------------------------------------------------------
    # Canonical Phonetic Key
    # ---------------------------------------------------------

    @staticmethod
    def canonical_phonetic_key(
        name: Optional[str],
    ) -> str:
        """
        Example

        John William Smith

        →

        JOHN_S530
        """

        if not name:
            return ""

        first = PhoneticUtils.first_name(name).upper()

        surname = PhoneticUtils.last_name(name)

        code = PhoneticUtils.soundex(surname)

        return f"{first}_{code}"

    # ---------------------------------------------------------
    # Phonetic Similarity
    # ---------------------------------------------------------

    @staticmethod
    def phonetic_similarity(
        left: Optional[str],
        right: Optional[str],
    ) -> float:
        """
        Returns

        1.0  = identical

        0.5  = partial phonetic match

        0.0  = different
        """

        if not left or not right:
            return 0.0

        if (
            PhoneticUtils.soundex(left)
            ==
            PhoneticUtils.soundex(right)
        ):
            return 1.0

        if PhoneticUtils.metaphone_match(left, right):
            return 0.75

        left_initial = PhoneticUtils.initials(left)
        right_initial = PhoneticUtils.initials(right)

        if left_initial == right_initial:
            return 0.50

        return 0.0

    # ---------------------------------------------------------
    # Phonetic Index
    # ---------------------------------------------------------

    @staticmethod
    def build_phonetic_index(
        names: List[str],
    ) -> dict[str, List[str]]:
        """
        Build an index using canonical phonetic keys.
        """

        index: dict[str, List[str]] = {}

        for name in names:

            key = PhoneticUtils.canonical_phonetic_key(name)

            index.setdefault(key, []).append(name)

        return index

    # ---------------------------------------------------------
    # Best Phonetic Candidates
    # ---------------------------------------------------------

    @staticmethod
    def phonetic_candidates(
        target: str,
        names: List[str],
        threshold: float = 0.75,
    ) -> List[str]:
        """
        Return names whose phonetic similarity
        exceeds the threshold.
        """

        matches = []

        for candidate in names:

            score = PhoneticUtils.phonetic_similarity(
                target,
                candidate,
            )

            if score >= threshold:
                matches.append(candidate)

        return matches