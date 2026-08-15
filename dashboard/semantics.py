"""
Compatibility facade for legacy semantic-layer imports.

Agents in this repository historically imported from a top-level semantics
module. The real implementation now lives in schema.py and loader.py, so this
module re-exports the public API to keep existing imports working while the
backend is refactored to use the injected SemanticLoader.
"""

from loader import DEFAULT_SEMANTIC_LAYER_PATH, SemanticLoader, SemanticMatch, get_semantic_loader, load_semantic_layer
from schema import *  # noqa: F401,F403
