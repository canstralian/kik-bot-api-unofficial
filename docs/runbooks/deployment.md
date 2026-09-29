# Deployment runbook (future gated application)

The protocol library is not the AI deployment. Deploy the separate governed bot application only after an authorised transport-compatibility receipt and a simulated app test. Use a dedicated test Kik account, explicitly allowed test group and secret-store/environment injection. Keep bot admin capability disabled for ordinary conversation, command/mention trigger required, bounded retention/rates, and health checks that distinguish CONNECTING, STREAM_READY, AUTHENTICATED and DEGRADED. No raw packet logging.

Rollout: simulated transport -> permitted test group -> monitored limited group trial -> separately approved Public Group. Roll back by stopping the app and preserving the redacted inbox/outbox ledger, not by blindly resending uncertain outbound messages. Never weaken TLS or spoof integrity controls to make a deployment succeed.

This runbook is a release gate document, not evidence that a live application has been deployed.
