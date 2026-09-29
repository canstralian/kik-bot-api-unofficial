# Protocol contracts — version 1 (synthetic adapter)

## Input contract
`normalize_stanza` takes exactly one complete UTF-8 XML stanza as `bytes`, maximum 65536 bytes. It rejects DTD, entity declarations and external references using defusedxml. Only message or IQ roots with no namespace, `jabber:client` or `kik:groups` are recognized. All event IDs are 1–128 safe identifier characters. Sender/recipient JIDs must pass existing Kik JID grammar.

## Normalised event
Immutable `ProtocolEvent` has `event_id, kind, sender_jid, recipient_jid, conversation_jid, body, receipt_type, receipt_ids, typing, media_app_id, iq_namespace, iq_status`. No raw XML or URL is included. A group event MUST carry a validated `g@jid`; its conversation key is the group JID, not the author. Direct events use the author JID as the conversation key.

## Supported synthetic cases
Direct/group text, direct/group delivered/read receipts (uniquely validated reference IDs), direct/group typing, media app metadata only, group status indicators and IQ result/error with allowlisted query namespace. A successful IQ response is not a permission grant. No interpretation of group administration occurs at this layer. Mention activation is application policy, not an inference from untrusted protocol attributes.

## Error contract
`ProtocolError` is raised for oversize/empty/broken XML, invalid namespace, unsupported event type, invalid identifier/JID, missing group route, duplicate or missing receipt references, invalid typing state and oversized/blank bodies. Its messages contain no untrusted XML content. The application must treat failures as deny/no outbound action. The parser never makes network calls.

## Current integration boundary
This is an independently testable parser and contract. It is not yet called from the existing `KikConnection.read_loop` or a guarantee that historical examples match a current Kik server. The legacy BeautifulSoup callback adapter remains until the governed integration phase, when event normalization, correlation and permissions are added as a separately tested change.
