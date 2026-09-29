"""Pure connection policy: deterministic retries and credential-safe endpoints."""
import re
from enum import Enum


class ConnectionState(str, Enum):
    STOPPED = "stopped"
    CONNECTING = "connecting"
    STREAM_READY = "stream_ready"
    AUTHENTICATING = "authenticating"
    AUTHENTICATED = "authenticated"
    BACKOFF = "backoff"
    TERMINAL = "terminal"



class KikDisconnectedError(RuntimeError):
    """An operation cannot proceed because its connection has stopped."""


def validate_endpoint(host, port=5223):
    """Fail closed: send credentials only to Kik-owned DNS hostnames."""
    if not isinstance(host, str) or not re.fullmatch(
        r"(?:[a-z0-9-]+\.)+kik\.com", host.lower()
    ):
        raise ValueError("endpoint must be a *.kik.com hostname (no scheme or path)")
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("port must be an integer between 1 and 65535")
    return host.lower(), port


def retry_delay(attempt, base_delay=2.0, maximum_delay=30.0, server_backoff=0.0):
    """Bounded exponential retry with server-directed backoff taking precedence."""
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
        raise ValueError("attempt must be a positive integer")
    if not 0 < base_delay <= maximum_delay:
        raise ValueError("invalid retry delay bounds")
    if server_backoff < 0:
        raise ValueError("server backoff cannot be negative")
    exponential = min(maximum_delay, base_delay * (2 ** min(attempt - 1, 16)))
    return max(exponential, float(server_backoff))
