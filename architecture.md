# SIGNOVA AI architecture and implementation plan

## Current request flow

Browser microphone → Web Speech API → editable transcript → FastAPI `/api/translate` → exact-match verified asset lookup → status response → UI status.

The backend deliberately does not claim to translate a spoken-language sentence into ISL. An exact phrase lookup is not a general language translation system.

## Target production pipeline

1. Streaming ASR with explicit language identification and timestamps.
2. Normalization that preserves negation, named entities, numbers, tense, discourse and uncertainty.
3. Semantic representation with provenance and confidence calibration.
4. ISL translation by a linguistically validated model / rule-and-model hybrid.
5. Native-signer review and evaluation across dialects and contexts.
6. Sign sequence planning with handshape, location, movement, orientation, non-manual markers and transitions.
7. Motion retargeting to a rigged avatar, with temporal alignment and quality checks.
8. Safe fallback to captions / clarification when a sign sequence is unsupported or uncertain.

## Sign asset policy

Each sign/motion item needs source provenance, usage rights, dialect/variant, gloss or semantic tags, handshape, location, movement, orientation, non-manual markers, temporal boundaries, reviewer identity/role, review date, and validation status. Do not use an asset until permission and review are documented.

## Evaluation

ASR: WER/CER by language, accent and noise condition.
Translation: semantic adequacy, negation/number/entity preservation, native-signer ratings and error taxonomy.
Animation: sign recognition back-testing, kinematic continuity, hand visibility/occlusion, facial/non-manual correctness.
Operations: p50/p95 latency, failure rate, device performance and privacy audit.
