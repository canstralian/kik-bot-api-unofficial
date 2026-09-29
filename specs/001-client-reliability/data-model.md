# Data model and contracts — 001

## ClientProfile (selected at process startup)
`kik_version: str` with four numeric components; `classes_dex_sha1_digest: str` canonical base64 whose decoded size is exactly 20 bytes. Validation establishes structure only, not genuine APK provenance or service acceptance. Legacy `kik_version_info` remains a read-only mapping.

## Endpoint
`host: str` must match a subdomain under `kik.com` and cannot be a URL or IP address; `port: int` 1..65535. If no override is supplied, legacy derivation is used and may be unreachable. TLS certificate validation and SNI use this same host.

## ClientSession
`connection_state: ConnectionState` has STOPPED, CONNECTING, STREAM_READY, AUTHENTICATING, AUTHENTICATED, BACKOFF, TERMINAL. `connected` denotes protocol stream acceptance, `authenticated` denotes authenticated session acknowledgement. Do not conflate them. `_auth_deadline` and timeout values are monotonic seconds. `_shutdown_event` broadcasts permanent termination; `_server_backoff_seconds` feeds next retry. `_last_connection_failure` records a coarse reason without payloads.

## Result semantics
A send raises KikDisconnectedError or TimeoutError on shutdown/deadline. Profile/image upload returns a Future; Future.result() surfaces transport/HTTP failure. Callback decorator returns Future and applies a bounded queue, preserving submission order. No successful result is recorded before confirmed completion.

## Transport failure taxonomy
DNS: resolution failed. TLS: certificate or handshake failed (no downgrade). TRANSPORT: remaining socket/OSError. TIMEOUT: connect, stream or authentication response exceeded deadline. PROTOCOL: unexpected parse/processing error. SERVER_BACKOFF: honour requested delay. BAD_VERSION: terminal until explicitly reconfigured and revalidated.

## Interface compatibility
Additional KikClient constructor options are appended to preserve positional arguments. Callback decorator return type changes from Thread to Future; callers must migrate any `.join()` to `.result(timeout=...)`. Photo helper returns Future rather than None. No external API guarantee is implied.
