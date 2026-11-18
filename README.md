# Task-availability evaluation records

Materials accompanying **Evaluating Payload-Dependent Task Loss in Adapted Agent Defenses** (R6).

## Files

- `paper_R6_2026-11-17.pdf`: current manuscript candidate.
- `paper_source_R6.zip`: editable manuscript source.
- `anonymous_artifact_R6.zip.part00` through `.part97`, `ARCHIVE_PARTS.json` and `assemble_artifact.py`: losslessly split 512-KiB transport of the complete saved-record artifact, including historical configurations, the fresh 328-cell panel, core execution audits, scripts and manifests.
- `CORE_FOUR_CELL_MATRIX.csv`: selected all-arm audit index.
- JSON reports document manuscript, bibliography, visual and pattern checks at the R6 freeze.
- `SHA256SUMS` and `RELEASE_MANIFEST.json`: transport integrity checks.

## Download and resume

The anonymous host may reset long transfers and does not support byte-range resume. Download the small parts and assemble the original archive with:

```sh
python3 download_artifact.py
```

This makes public file requests, verifies every part, and reuses verified parts when rerun. It does not require login, model keys or paid inference. The default is two concurrent requests. Then extract `artifact_download/anonymous_artifact_R6.zip` and run the offline checks below. A full repository ZIP is optional.

## Offline verification

Use Python 3.10 or newer:

```sh
python3 assemble_artifact.py
python3 -m zipfile -e anonymous_artifact_R6.zip artifact
cd artifact/anonymous_artifact_R6
python3 verify_all.py
```

The verifier checks distribution hashes and five groups of saved-record consistency checks (the historical group includes ten internal layers). It does not call models, require API keys, rerun online agents or certify independent semantic correctness. Simulator replay is a separate environment-dependent check documented in the bundle.

## Scope

Main positive results concern adapted detector/enforcement configurations. The full native validation and official-path limitations are retained, together with technical missing cells and non-independent comparisons. Source judgments remain author/AI inspections. Saved payload text is experimental data, not instructions to execute. Original third-party notices and licenses are retained inside the bundle.

The R6 manuscript is frozen: its Open Science section still marks the anonymous review URL as pending. This source repository is a hosting source, not an anonymous review address. Hosting completion and final submission are separate steps.
