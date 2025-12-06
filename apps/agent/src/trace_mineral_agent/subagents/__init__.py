"""Subagents for TraceMineralDiscoveryAgent."""

from .allopathy import allopathy_subagent
from .naturopathy import naturopathy_subagent
from .ayurveda import ayurveda_subagent
from .tcm import tcm_subagent
from .synthesis import synthesis_subagent

__all__ = [
    "allopathy_subagent",
    "naturopathy_subagent",
    "ayurveda_subagent",
    "tcm_subagent",
    "synthesis_subagent",
]
