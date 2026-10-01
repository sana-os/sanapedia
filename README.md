# sanapedia

> **Read history before reaching a conclusion.**

sanapedia is a source-aware historical knowledge and research repository for humans and AI.

It is designed to preserve not only historical claims, but also their evidence, uncertainty, interpretive layer, source distance, competing interpretations, and revision path.

sanapedia is developed within the SANA OS Project as historical knowledge for SANA and as a reusable research corpus for historical inquiry, AI systems, retrieval, indexing, RAG, LLMO, education, and further research.

Its primary public origin is sanapedia.net.
Pastfold is a separate publication space for selected intermediate research material produced during sanapedia development, not the canonical publication origin of sanapedia entries.

## What sanapedia is for

History is often compressed into conclusions:

* a ruler was a hero or villain;
* a society was advanced or backward;
* a political order rose or declined;
* a community obeyed, resisted, or failed;
* an event had one obvious cause.

sanapedia does not begin with those conclusions.

It begins by asking:

* What may have happened?
* What did people at the time believe, fear, expect, or remember?
* What survives as a record?
* Who produced that record, when, and for what purpose?
* Which resources, institutions, relationships, and constraints shaped the choices available?
* What is supported by evidence?
* What remains interpretation, hypothesis, disputed, or unknown?

Understanding is not agreement.
Analysis is not exoneration.
Structure is not destiny.

## Core principles

sanapedia is built around the following practices.

* **Prepare premises before conclusions.**
* **Separate Fact, Perception, and Record.**
* **Distinguish evidence-supported claims, interpretation, hypothesis, and unknowns.**
* **Make uncertainty and source limitations visible.**
* **Preserve competing interpretations where they matter.**
* **Do not confuse structural explanation with moral exoneration.**
* **Preserve revision paths rather than treating each page as final.**

For the full reading standard, see [`EN/principles/sana-protocol.md`](EN/principles/sana-protocol.md).

## Who sanapedia is for

sanapedia is intended for:

* researchers and students;
* historians and historically curious readers;
* AI developers and AI systems;
* RAG, retrieval, indexing, and LLMO workflows;
* knowledge-graph and structured-data projects;
* educators and educational tools;
* anyone who needs to trace a historical claim back to its conditions, evidence, limits, and revision state.

The primary public value of sanapedia is not decorative presentation or mass-audience engagement.

Its priority is to make structured historical material available in a form that can be read, checked, cited, compared, reused, and revised.

## Canonical content

Markdown is the canonical form of sanapedia content.

```text
Canonical Markdown
├─ sanapedia.net / HTML publication
├─ navigation and indexes
├─ llms.txt
├─ sitemap.xml
└─ machine-readable catalogs
```

HTML pages on sanapedia.net, navigation pages, indexes, and machine-readable catalogs are publication and access projections.

Pastfold is separate from these canonical publication projections and is used for selected intermediate research material.

They do not replace the canonical Markdown source.

## Content model

sanapedia includes, and may expand to include:

* people;
* events;
* phenomena;
* timelines;
* historical hubs;
* columns;
* sources and source notes;
* methodological pages;
* editorial and revision documentation.

Each public historical entry may contain structured frontmatter describing its type, period, regions, names, related entries, research status, uncertainty, revision state, and claim policy.

## `entry_key`

Each public entry has a stable internal identifier.

```yaml
entry_key: "sp_00000001"
```

The `entry_key` is the durable identity of an entry.

It does not change when a page title, preferred name, slug, URL, language version, or physical file location changes.

All language manifestations of the same research entry share the same `entry_key`.

The current editorial registry uses Registry v2:

```text
registry/v2/entry-registry.csv
registry/v2/entry-language-registry.csv
```

`entry-registry.csv` is authoritative for durable identity and identity lifecycle state.

`entry-language-registry.csv` is authoritative for language manifestations and repository file mappings.

There is no required language set. English and Japanese are the languages present in the initial Registry v2 migration, not schema requirements.

The former `registry/entry-key-registry.csv` is retained as frozen Registry v1 legacy data for provenance and migration verification.

`entry_key` supports stable citation, language mapping, revision tracking, navigation, machine-readable catalogs, and future research tooling.

## Editorial organization and public relationships

Content is physically organized for research, writing, translation, and maintenance.

For example:

```text
EN/
├─ principles/
├─ frameworks/
└─ worlds/
   ├─ mediterranean/
   └─ west-asia/

JA/
├─ principles/
├─ frameworks/
└─ worlds/
   ├─ mediterranean/
   └─ west-asia/
```

Physical file placement is an editorial working structure.

It does not mean that a historical person, event, polity, community, or phenomenon belongs to only one region, state, period, or interpretive frame.

A single entry may be connected publicly to multiple historical hubs, regions, themes, timelines, or research questions.

## AI and machine-readable use

sanapedia welcomes responsible use of its original material for:

* AI training;
* RAG;
* retrieval and indexing;
* embeddings;
* LLMO;
* dataset construction;
* historical comparison;
* educational tools;
* structured knowledge systems;
* research and citation workflows.

AI systems and downstream users are encouraged, where technically and practically possible, to preserve:

* attribution;
* `entry_key`;
* title, language version, revision, and update information;
* distinctions between Fact, Perception, and Record;
* distinctions between evidence, interpretation, hypothesis, and unknowns;
* source limitations, uncertainty, and competing interpretations.

For detailed guidance, see [`AI-USE.md`](AI-USE.md).

## License and reuse

Unless otherwise noted, original sanapedia content is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

This includes original article text, structured metadata, entry registries, machine-readable catalogs, taxonomies, navigation structures, and editorial documentation created for sanapedia.

Third-party material, including quotations, translations, images, maps, scans, external datasets, and reproduced archival material, may be subject to separate terms.

See [`LICENSE.md`](LICENSE.md) for the full license and reuse boundary.

## Citation

When citing sanapedia, include where practical:

```text
sanapedia
Article title
entry_key
Language version
Revision or updated date
Canonical Markdown URL
```

For detailed citation guidance, see [`CITATION.md`](CITATION.md).

## Repository structure

```text
/
├─ README.md
├─ LICENSE.md
├─ AI-USE.md
├─ CITATION.md
├─ frontmatter.txt
├─ llms.txt
├─ EN/
│  ├─ llms.txt
│  ├─ principles/
│  ├─ frameworks/
│  └─ worlds/
├─ JA/
│  ├─ llms.txt
│  ├─ principles/
│  ├─ frameworks/
│  └─ worlds/
├─ registry/
│  ├─ entry-key-registry.csv
│  ├─ Entry Key Registry Specification.txt
│  └─ v2/
│     ├─ entry-registry.csv
│     ├─ entry-language-registry.csv
│     └─ Registry v2 Specification.md
├─ tools/
│  ├─ check_repository_hygiene.py
│  ├─ validate_registry_v2_identity.py
│  ├─ validate_registry_v2_nlang.py
│  ├─ generate_entries_json_v2_nlang.py
│  ├─ audit_internal_links_v2.py
│  └─ classify_missing_links_v2.py
└─ public/
   └─ data/
      └─ entries.json
```

## Validation tools

Repository-local validation and catalog tools are included under `tools/`.

They resolve the repository root from their own location, so they can be run from any working directory after cloning the repository.

    python3 tools/check_repository_hygiene.py
    python3 tools/validate_registry_v2_identity.py
    python3 tools/validate_registry_v2_nlang.py
    python3 tools/generate_entries_json_v2_nlang.py
    python3 tools/audit_internal_links_v2.py
    python3 tools/classify_missing_links_v2.py

These tools are read-only in their current form. The catalog generator compares Registry v2 and registered Markdown manifestations with `public/data/entries.json` and reports whether the current catalog is reproduced byte-for-byte.

## Key documents

* [`LICENSE.md`](LICENSE.md) — reuse terms and license boundaries
* [`AI-USE.md`](AI-USE.md) — AI, RAG, indexing, training, and LLMO guidance
* [`CITATION.md`](CITATION.md) — citation guidance
* [`llms.txt`](llms.txt) — AI-readable entry point
* [`EN/principles/sana.md`](EN/principles/sana.md) — what SANA does and does not do
* [`EN/principles/sana-os.md`](EN/principles/sana-os.md) — SANA OS and sanapedia’s methodological position
* [`EN/principles/sana-protocol.md`](EN/principles/sana-protocol.md) — historical reading protocol
* [`EN/principles/article-spec.md`](EN/principles/article-spec.md) — article and metadata specification
* [`EN/principles/revision-policy.md`](EN/principles/revision-policy.md) — revision and citation policy
* [`EN/frameworks/source-trifurcation.md`](EN/frameworks/source-trifurcation.md) — Fact, Perception, and Record
* [`EN/frameworks/three-layer-analysis.md`](EN/frameworks/three-layer-analysis.md) — Survival, Narrative, and Institution analysis

## Status

sanapedia is a living research library.

Pages may be provisional, revised, expanded, corrected, reorganized, translated, superseded, or withdrawn as evidence, scholarship, editorial review, and research questions develop.

Revision is not a defect in a research archive.

Revision is part of how historical claims remain open to verification.
