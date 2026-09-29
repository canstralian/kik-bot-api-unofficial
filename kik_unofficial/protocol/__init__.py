"""Synthetic, offline-testable Kik protocol event normalization."""
from .events import EventKind, ProtocolError, ProtocolEvent, normalize_stanza

__all__ = ["EventKind", "ProtocolError", "ProtocolEvent", "normalize_stanza"]
