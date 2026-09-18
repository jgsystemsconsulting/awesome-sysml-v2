# Research: awesome-magicgrid-mbse ecosystem scan

Date: 2026-09-17. Method: web research subagent (33 tool uses, search plus targeted
fetches). Purpose: assess whether a curated awesome list for the MagicGrid MBSE
methodology has enough linkable material, and what shape it should take.

## 1. Existing coverage

- No public `awesome-magic-grid`, `awesome-magicgrid`, or similar list exists
  (GitHub repo search: 0 hits).
- Nearby lists, none covering the methodology well:
  - jgsystemsconsulting/awesome-sysml-v2 (SysML v2 language and tooling)
  - mycr0ft/awesome-sysml (SysML tooling)
  - kktse/awesome-systems-engineering (general SE)
  - ishandutta2007/Awesome-MBSE-Engineer-Interview-QA (interview Q&A)
- jgsystemsconsulting/awesome-mbse exists but is private.
- GitHub "MagicGrid" repos are almost all CSS/JS grid libraries or empty stubs.
  Rare real MBSE hit: matthieugourssies/sysml-magicgrid-vccs. The `magicgrid`
  GitHub topic is unused for MBSE.
- Gap is real: no methodology-focused list. Overlap with SysML v2 lists is low
  (language and tooling versus method and grid).

## 2. Resource buckets (publicly linkable, credible)

| Bucket | Estimated count | Notes |
|--------|-----------------|-------|
| Official | 8-15 | Product and training pages strong; deep MagicGrid doc URLs brittle |
| Books and formal publications | 2-5 | BoK core; Edition 2 referenced in vendor media |
| Academic papers | 15-30 | ~7 strong title hits; ~20+ body or case-study mentions |
| Training | 5-15 | Official catalog plus partners and seminars |
| Blogs and walkthroughs | 5-20 | Independent blogs thin; video-led tutorials stronger |
| Videos and talks | 15-40 | Best open surface area |
| Tools and models | 3-8 | Mostly the Dassault stack plus a few sample models |
| Community | 5-10 | INCOSE-centric; weak open forums and tags |

Roll-up: roughly 40-70 linkable items inclusive; core high-signal set 35-50.

### Official examples

- https://www.3ds.com/products/catia/catia-magic (CATIA Magic product family)
- https://www.3ds.com/products/catia/no-magic (No Magic / Cameo hub)
- https://www.3ds.com/products/catia/no-magic/cameo-systems-modeler
- https://docs.nomagic.com/ (documentation hub; still on docs.nomagic.com)
- https://www.3ds.com/edu/catia-magic-training (training catalog)
- https://www.3ds.com/edu/catia-magic-training/mbse-sysml-v2-and-magicgrid
  ("MBSE with SysML V2 and MagicGrid" 3-day course, refreshed for CATIA Magic
  2026x per page metadata around Dec 2025)
- Catalog also lists "Applying MBSE with SysML and MagicGrid".
- Top-level CATIA Magic marketing pages scraped contain zero mentions of
  MagicGrid; the method lives in training, docs, and papers.
- Old `nomagic.com/mbse/magicgrid` URL returns 403.

### Books

- MagicGrid Book of Knowledge (2018), by Aiste Aleksandraviciene et al.,
  Vitae Litera, ~172 pp. Goodreads:
  https://www.goodreads.com/book/show/56720281-magicgrid-book-of-knowledge
- Edition 2 referenced in vendor videos. Open Library: 0 title hits
  (discoverability outside vendor channels is poor).

### Academic examples (INCOSE / Wiley / Springer / ACM)

- MBSE Grid origin paper (2017): https://doi.org/10.1002/j.2334-5837.2017.00350.x
- Towards a Common SE Methodology (2020): https://doi.org/10.1002/j.2334-5837.2020.00713.x
- V&V using MagicGrid (INSIGHT 2023): https://doi.org/10.1002/inst.12429
- SysML v1 vs v2 in MagicGrid scope (2024): https://doi.org/10.1002/iis2.13257
- Architecture meta-model for MagicGrid (2024): https://doi.org/10.1002/iis2.13284
- Extending MagicGrid for virtual prototyping (ACM 2024): https://doi.org/10.1145/3652620.3686249
- SysML v2 solution architecture with MagicGrid (2025): https://doi.org/10.1002/iis2.70000
- Flight-control requirements case (Springer 2024): https://doi.org/10.1007/978-981-97-0550-4_3
- Space remote-sensing case (Springer 2020): https://doi.org/10.1007/978-981-33-4102-9_35
- Mainstream MBSE methodologies survey (2022): https://doi.org/10.3233/faia220529
- OpenAlex title filter "MagicGrid": 7 works; body mentions ~20-25 usable
  after culling. ArXiv: 0.

### Training and video examples

- Official course and catalog links above.
- MagicGrid SysML methodology walkthrough: https://youtu.be/todMOBqirAA
- "SysML Made Simple with MagicGrid" full seminar: https://youtu.be/xFGFA8H7Yd0
  (Morkevicius et al.)
- BoK Edition 2 video: https://youtu.be/FzrzzSS4GvM
- MoEs / traceability: https://youtu.be/CsF2nKbO0KY
- Conceptual subsystems: https://youtu.be/UzNZhFSGtjw
- Radar sample model: https://youtu.be/JtWZQM-yamk
- Hypermodeling: MagicGrid: https://youtu.be/0ctdRBGiBk0
- Non-English (e.g. Korean) CATIA Magic + MagicGrid tutorial series also exist.

### Tools and community

- Implementers in practice: CATIA Magic / Cameo Systems Modeler / MagicDraw
  only. Capella-Arcadia, OOSEM, Harmony-SE are peer methodologies, not ports.
- Sparse public sample models (Cameo project samples, student repos).
- Community: INCOSE symposium track, Cameo/No Magic LinkedIn circles, no
  strong Stack Exchange tag. mbse4u.com mentions MagicGrid but has little
  durable post inventory.

## 3. Trademark and naming

- MagicGrid is vendor methodology branding (No Magic, now Dassault Systemes):
  BoK title, course names, INCOSE papers by vendor-affiliated authors.
- No evidence of enforcement against descriptive community use; no community
  trademark free-for-all either. Standard awesome-list posture (descriptive
  use plus disclaimer) is the safe shape.
- Bigger practical issue is name collision: GitHub and search "MagicGrid" is
  dominated by CSS/JS grid libraries. Prefer `awesome-magicgrid-mbse` over a
  bare `awesome-magic-grid`.
- README disclaimer recommended: not affiliated with Dassault Systemes or
  No Magic; MagicGrid may be their trademark.

## 4. Ecosystem health (2024-2026)

- Not dead: INCOSE papers 2022-2025 including SysML v2 + MagicGrid work; the
  official SysML V2 + MagicGrid course was refreshed for CATIA Magic 2026x in
  late 2025.
- Acquisition trail: No Magic bought by Dassault Systemes; public face is now
  CATIA Magic / Cameo; nomagic.com folds into 3ds.com; docs remain on
  docs.nomagic.com. MagicGrid still names training and research; it is
  under-mentioned on top-level product marketing pages.
- Lineage: MBSE Grid paper (2017) to MagicGrid BoK (2018) to ongoing framework
  papers and SysML v2 adaptation.
- Health profile: vendor-sustained plus academic, not grassroots open source.
  Weaker "new independent blog every month" signal than SysML v2 tooling.

## Verdict

| Question | Answer |
|----------|--------|
| Enough material for a niche awesome list (bar ~40+ links)? | Yes, barely to moderately: 40-70 reachable with videos, papers, and official pages included |
| Sustainable like awesome-sysml-v2? | Weaker: single-vendor method, paywalled literature, brittle doc URLs |
| Standalone build? | Viable niche for methodology depth, accepting vendor gravity |
| Alternative | A MagicGrid section inside a broader awesome-mbse list ages better but that repo is currently private |

Decision from conversation (2026-09-17): build standalone
`awesome-magicgrid-mbse` now, cross-linked with awesome-sysml-v2; fold into a
public awesome-mbse later only if that repo goes public.

## Risks

1. Single-vendor dependence: list quality tracks Dassault publishing.
2. Paywalls and registration walls: many best papers (Wiley, Springer); some
   tool docs account-gated.
3. Link rot: guessed MagicGrid doc paths 404; old nomagic.com URLs 403.
4. Name collision: CSS MagicGrid libraries swamp GitHub and search.
5. Copyright: never host BoK PDFs; link legitimate sales or library pages.
6. Maintenance load: fewer spontaneous community PRs than a language list.
