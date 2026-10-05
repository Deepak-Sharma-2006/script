---
name: code-reading-dossier
description: >-
  Generates comprehensive cognitive code reading dossiers using the 6-Technique Cognitive Reading Protocol.
  Use this skill at the end of each development phase or when a human operator needs to deeply understand,
  audit, or review newly authored agent code.
---

# Cognitive Code Reading Dossier Generator

This skill extracts deep mechanical and architectural comprehension from source code, converting complex implementation files into structured mental models for the human operator.

## The 6 Mandatory Techniques

1. **Technique 1: The Human Mental Model**
   - 2–3 paragraphs defining real-world purpose, explicit responsibilities, and clear boundaries.
2. **Technique 2: Visual Code Flow (The Call Graph)**
   - ASCII or Mermaid diagram tracing: Inbound Request \rightarrow Middleware \rightarrow Service \rightarrow DB \rightarrow Egress.
3. **Technique 3: Variable Lifecycle Trace (Follow the Data)**
   - Tracing the core domain variable through Birth, Mutation, Packaging, and Egress.
4. **Technique 4: Non-Blocking Noise Filtering**
   - Explicitly cataloging non-blocking loggers, metrics, and middleware bypassed during Pass 1 reading.
5. **Technique 5: Audit Exactly One Failure Path**
   - Auditing account enumeration risks and timing attack differentials (\Delta t) on credential/token checks.
6. **Technique 6: The 1-Sentence Feynman Mental Compression Test**
   - Compressing the entire implementation into one clear, dense sentence.

## Output Target
Save the completed dossier to:
`docs/dossiers/phase-<X>-<domain>.md`
