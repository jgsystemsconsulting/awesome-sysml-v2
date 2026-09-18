# Landing truth freeze

Product contract for the Path S GitHub Pages router (`docs/index.html`).
The release gate (`scripts/check_release.py`) enforces this on every push and
pull request to main via `.github/workflows/validate.yml`.

## Sources of truth

| Landing surface | Source | Gate rule |
| --- | --- | --- |
| chip `version` | `RELEASE-INFO.txt` field `Version:` | Exact string match |
| chip `sweep` | README badge `![Last full sweep: YYYY-MM]` | Exact YYYY-MM match |
| chip `entries` | Count of grammar-valid bullets under the eleven curated README `##` sections | Integer equality |
| section-index href fragments | The eleven curated README heading titles, GitHub-slugified | Order and slug match |

## Frozen chip `dt` names

Display labels on the landing may change. These `dt` names are gate inputs and
must not be renamed without updating the gate:

- `version`
- `sweep`
- `entries`

## Curated sections (order fixed)

1. Specifications and Standards
2. Official Implementations
3. Editors and Language Tooling
4. Modeling and Visualization
5. Parsers, SDKs, and API Clients
6. Validation and Analysis
7. Models and Case Studies
8. Learning Resources
9. Deployment and Containers
10. Commercial Tools
11. Migrating from SysML v1

Heading renames require a matching section-index and gate `CURATED_SECTIONS`
update in the same change.

## Maintainer write path

1. Edit README entries or headings (or bump `RELEASE-INFO.txt` Version).
2. Update the matching landing chip and/or section-index row in `docs/index.html`.
3. Run `python scripts/check_release.py` from the repository root.
4. Open the PR; validate.yml must stay green.
