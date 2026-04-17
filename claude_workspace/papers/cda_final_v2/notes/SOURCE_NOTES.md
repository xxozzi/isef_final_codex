# CDA Final V2 Source Notes

## Canonical Project Inputs

- Scientific predecessor: `claude_workspace/papers/CDA_final/main.tex`
- Style basis: `claude_workspace/papers/cda_final_v2/neurips_2021.sty`
- Local inspiration sources:
  - `literature/swad_tex_source/0.abstract.tex`
  - `literature/diwa_tex_source/sections/00_abstract.tex`
  - other local source trees in `literature/` as needed for structure and citations

## Author / Affiliation Facts

- Jayden Jeong
  - Affiliation: Math, Science, and Technology Center (MSTC), Paul Laurence Dunbar High School, Lexington, Kentucky, USA
  - Email: `jayden.w.jeong@gmail.com`
- Vijayan K. Asari
  - Affiliation: School of Engineering, Department of Electrical and Computer Engineering, University of Dayton, Dayton, Ohio, USA
  - Additional lab affiliation: Vision Lab, Center of Excellence for Computational Intelligence and Machine Vision
  - Email: `vasari1@udayton.edu`

## Verified Web Sources

- University of Dayton directory page for Vijayan K. Asari:
  - <https://udayton.edu/directory/engineering/electrical-and-computer/asari_vijayan.php>
- University of Dayton Vision Lab team page:
  - <https://udayton.edu/centers/vision-lab/team.php>
- MSTC page:
  - <https://pld.fcps.net/mstc>

## Structural Targets

- Section order:
  - Abstract
  - Introduction
  - Related Work
  - Theory / Theoretical Motivation
  - Method + Setup
  - Experiments
  - Discussion
  - Limitations
  - Conclusion
  - Acknowledgements
  - References
  - Appendix
- The abstract is written last.
- The method section contains an empirical-analysis subsection.
- Proofs and long derivations go to the appendix by default.

## Drafting Model

- Canonical layer:
  - approved values supplied by Dr. Asari
- Provisional layer:
  - red values
  - red claims
  - red captions
  - red discussion spans
- Submission mode must fail if any provisional layer content survives.

## Immediate Writing References

- SWAD abstract pattern:
  - problem
  - gap
  - method
  - evidence
  - takeaway
- DiWA abstract pattern:
  - problem
  - high-level mechanism
  - theoretical lens
  - empirical outcome

## Keep / Remove Heuristics

- Keep:
  - the core CDA selector-weighting logic
  - the strongest theoretical motivation
  - definitions that are needed to make the certificate and canalization story legible
  - real benchmark tables supplied by Dr. Asari
- Remove or rewrite:
  - internal names such as `DCOLA`
  - defensive prose
  - reviewer-facing prose
  - duplicated explanations of the pipeline
  - theorem-shaped filler
  - implementation-detail clutter in the main body
