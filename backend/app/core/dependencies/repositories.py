"""
Repository Dependency Providers
"""

from functools import lru_cache

from app.services.graph.neo4j import get_neo4j_driver

from app.services.shell_detection.shell_pattern_repository import (
    ShellPatternRepository,
)


@lru_cache
def get_shell_pattern_repository() -> ShellPatternRepository:

    return ShellPatternRepository(
        driver=get_neo4j_driver(),
    )