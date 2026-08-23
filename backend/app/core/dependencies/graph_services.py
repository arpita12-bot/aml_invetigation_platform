"""
Graph Service Dependencies
"""

from functools import lru_cache

from app.services.shell_detection.shell_pattern_scoring import (
    ShellPatternScoring,
)

from app.services.shell_detection.shell_pattern_explainer import (
    ShellPatternExplainer,
)

from app.services.shell_detection.shell_pattern_materializer import (
    ShellPatternMaterializer,
)

from app.core.dependencies.repositories import (
    get_shell_pattern_repository,
)


@lru_cache
def get_shell_pattern_scoring():

    return ShellPatternScoring()


@lru_cache
def get_shell_pattern_explainer():

    return ShellPatternExplainer()


@lru_cache
def get_shell_pattern_materializer():

    return ShellPatternMaterializer(

        repository=get_shell_pattern_repository(),

        scoring=get_shell_pattern_scoring(),

        explainer=get_shell_pattern_explainer(),

    )