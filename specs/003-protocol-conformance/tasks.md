# Tasks — 003

- [x] P201 Define event model and parser rejection contract.
- [x] P202 Implement namespace-aware, bounded, side-effect-free normalizer.
- [x] P203 Add synthetic direct/group, receipt, typing, media, status and IQ fixtures.
- [x] P204 Add negative tests for DTD, entity, namespace, JID, receipt IDs, message type and limits.
- [x] P205 Initial protocol CI at f8559f2: 35 offline tests per Python 3.10 and 3.11, strict third-party dependency audit, package/wheel verification and Docker build passed (Actions run 36571522205). Any subsequent documentation commit requires its own final-head receipt before merge.
- [ ] P206 Review the adapter and decide how to bridge it into the legacy streaming callback layer in a subsequent PR.
- [ ] P207 Extend event processing with durable inbox/outbox, policy authorization and acknowledgement correlation (feature 004).

Note: completion of fixtures is not live authentication or a merge approval.
