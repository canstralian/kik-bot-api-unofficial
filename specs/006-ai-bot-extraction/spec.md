# Feature 005 — Separately deployable AI bot (planned)

The application is a separate deployment/repository from the reusable transport library. Define a transport adapter, command/mention router, policy engine, provider interface (hosted/Local/Dialogflow optional), bounded context retention, SQLite inbox/outbox and redacted operational events. Ordinary conversation never needs group-admin authority; LLM output cannot directly invoke privileged Kik operations. Simulate bot-author self-message, duplicate inbound message, rate exhaustion, wrong group route, provider timeout, disconnected transport and ambiguous send. Release requires simulated behaviour first and an authorised test-group roundtrip after transport compatibility is proven.

Proposed target repository: `canstralian/kik-ai-group-bot`; repository creation/deployment is a separate action. This spec does not claim that the repository already exists.
