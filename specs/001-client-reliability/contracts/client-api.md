# Interface contract — Client lifecycle and uploads

Version: feature 001 | Compatibility: intentionally amended, see README.

## Client constructor
`KikClient(callback, kik_username, kik_password, kik_node=None, device_id=None, android_id=None, log_level=20, enable_console_logging=False, log_file_path=None, disable_auth_cert=True, host=None, port=5223, connect_timeout=10.0, initial_response_timeout=15.0, login_response_timeout=20.0, message_wait_timeout=20.0)`

Validation occurs before the connection thread begins. `host`, if supplied, must be a DNS name under `*.kik.com`; `port` must be 1..65535. Timeouts must be positive and at most 3600 seconds. The selected client profile must pass structural validation. No constructor call can guarantee login.

## Lifecycle
`wait_for_messages(max_retries=5)` joins the initial connection and performs up to `max_retries` additional attempts. It never recursively spawns more attempts. Delays are exponential with a local 30-second ceiling, unless the server explicitly requests a longer delay. Invalid max_retries raises ValueError. Explicit version rejection or permanent disconnect prevents further attempts. Read `connection_state` for stage and `_last_connection_failure` for diagnostic category; internal underscore fields are observational only and not promised stable API.

`disconnect(permanent=True)` stops the supervisor and wakes waiting outbound operations. `disconnect(permanent=False)` permits a supervisor-managed session turnover. If callers do not enter `wait_for_messages`, they should not expect automatic recovery.

## Outbound API
`send_chat_message(...)` returns message ID when packet submission is queued, not a delivery receipt. It raises TimeoutError on missing connection deadline and KikDisconnectedError after terminal shutdown. Protocol login and ping are permitted before authenticated session where explicitly required by the protocol.

## Media
Profile-picture and gallery-upload helpers return concurrent.futures.Future; `.result(timeout=...)` surfaces HTTP failure and network exception. Chat-image transmission awaits upload completion before sending a dependent stanza. HTTP 200 is the implemented success response.

## Callback scheduler
`run_in_new_thread` now returns Future, not Thread; `.result()` replaces `.join()`. A single worker preserves submission order, with up to 64 outstanding callbacks. Saturation raises RuntimeError rather than allocating unlimited threads. Callback exception is exposed via Future and logged without payload.

## Trust boundary
No raw message text/credential stanzas are allowed in transport logs. TLS verification remains enabled. Kik's own login/verification results are authoritative; a locally syntactically valid fingerprint is not an attestation or capability token.
