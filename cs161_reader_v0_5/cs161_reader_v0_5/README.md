# CS161 Reader — v0.5 (Proof Pattern Consolidation)

v0.5 introduces a canonical proof pattern registry.
All theorems must reference one or more proof patterns.

## New in v0.5
- docs/proof_patterns.md (canonical definitions)
- Pattern taxonomy stabilized
- Chapters updated to reference pattern IDs

## Build
Markdown-first. Use Pandoc to build PDFs as before.

Example:
    pandoc chapters/ch04_randomized_algorithms.md -o ch04.pdf
