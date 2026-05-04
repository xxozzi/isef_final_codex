# Panel Review Round 4: Motivation Update

Date: 2026-04-30.

## Reason For Review

The previous motivation still risked circular reasoning because it motivated CDA from source-domain reweighting, source-domain composition changes, or the absence of CDA's own criterion in prior work. The revised framing moves the motivation outside CDA's mechanics.

## Revised Motivation Chain

1. **External problem:** source-only post-hoc checkpoint deployment can be underidentified by scalar source validation.
2. **General response:** preserve and use domain-wise source-risk evidence instead of immediately collapsing it to one average.
3. **CDA-specific hypothesis:** source-composition robustness is one conditional scalarization of that domain-wise evidence for mergeable checkpoint banks.

This sequence prevents the false argument that SWAD, DiWA, EoA, or model soups are worse because they did not optimize CDA's criterion.

## Council Verdicts

- **Reviewer A, motivation logic:** approved. The motivation now lies outside CDA's own mechanics and no longer depends on the old circular claim.
- **Reviewer B, literature fairness:** approved. The files do not imply that SWAD, DiWA, EoA, model soups, QRM, DRO, GroupDRO, WDRDG, or related work are inferior for not doing CDA.
- **Reviewer C, consistency:** approved. The active planning files and introduction scaffold consistently use the new order: scalar underidentification, domain-wise evidence, CDA as one conditional criterion.

## Active Files Confirmed

- `narrative.md`
- `misc/literature_notes/modern_literature_refresh.md`
- `finalization.md`
- `fixes.md`
- `src/02_introduction.tex`

## Final Status

The revised motivation is approved by the reviewer council. Manuscript drafting remains blocked until the empirical lineage, replay, table, and figure gates in `finalization.md` are completed.
