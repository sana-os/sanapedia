---
entry_key: "sp_00000051"
title: "Article Specification"
slug: "article-spec"
entity_type: "policy"
content_type: "policy"
status: "provisional"
revision: "0.2"
language: "en"
published: "2026-09-13"
updated: "2026-10-02"
---

# Article Specification

## 1. Purpose

This document defines the structural requirements of a public sanapedia knowledge page.

The specification exists to support:

- durable entry identity;
- language-specific manifestations;
- revision tracking;
- citation;
- canonical Markdown access;
- public publication;
- machine-readable catalogs;
- AI and retrieval use;
- editorial validation.

This specification defines page structure and metadata responsibilities.

It does not replace historical analysis.

Historical claims, evidence, interpretation, uncertainty, source limitations, competing interpretations, and hypotheses belong in the article body.

---

## 2. Core rule

Every registered public knowledge page must have:

1. a durable `entry_key`;
2. a language-specific Markdown manifestation;
3. valid frontmatter;
4. article content appropriate to its `entity_type` and `content_type`;
5. a Registry v2 mapping between identity, language, and file path.

The Markdown file is the durable knowledge source.

HTML pages, indexes, navigation, catalogs, sitemaps, and other publication outputs are derived projections.

---

## 3. Required metadata

Every public registered manifestation must include the following frontmatter fields.

### `entry_key`

The durable identity of the research entry.

Rules:

- required;
- quoted string;
- format: `sp_00000000`;
- must match Registry v2;
- must never be reused;
- must not encode language, geography, period, hierarchy, status, or entity type;
- all language manifestations of the same research identity share the same `entry_key`.

Changing a title, slug, URL, file location, editorial placement, or wording does not create a new identity.

### `title`

The display title of the specific language manifestation.

Rules:

- required;
- quoted string;
- language-specific;
- may change over time;
- does not determine identity.

### `language`

The language of the manifestation.

Rules:

- required;
- lowercase;
- quoted string;
- must agree with the Registry v2 manifestation mapping and language root.

The schema does not require a fixed set of languages.

### `status`

The lifecycle or editorial state of the entry.

Allowed values:

- `draft`
- `active`
- `provisional`
- `superseded`
- `redirected`
- `withdrawn`

Status may change without changing `entry_key`.

Withdrawn, redirected, or superseded identities must not be silently reused or deleted from the identity registry.

### `entity_type`

Describes what kind of entity or conceptual object the entry represents.

Allowed values:

- `person`
- `event`
- `timeline`
- `historical_hub`
- `phenomenon`
- `source`
- `column`
- `principle`
- `policy`
- `index`

`entity_type` may change if editorial understanding changes.

Such a change does not alter identity.

### `content_type`

Describes how the page functions within sanapedia.

Allowed values:

- `historical_entry`
- `historical_hub`
- `timeline`
- `policy`
- `principle`
- `index`
- `source_note`
- `column`

`entity_type` and `content_type` are related but distinct.

For example:

```yaml
entity_type: "event"
content_type: "historical_entry"
```

The first describes what the entry is about.

The second describes the function of the page.

### `revision`

The visible revision number of the specific language manifestation.

Rules:

- required;
- quoted string;
- may differ between language manifestations;
- should increase when substantive content changes;
- does not determine identity.

Typical early values include:

```text
0.1
0.2
0.3
1.0
1.1
```

Revision handling and citation practice are defined separately in the Revision and Citation Policy.

### `updated`

The date when the language manifestation was last materially updated.

Rules:

- required;
- quoted string;
- ISO format: `YYYY-MM-DD`;
- may differ between language manifestations;
- should change when claims, source notes, interpretation, structure, title, or status materially change.

---

## 4. Recommended metadata

The following fields are not required by the minimum schema but are recommended where relevant.

### `summary`

A short language-specific description for indexes, search results, previews, AI catalogs, and navigation.

A summary should not overstate certainty.

### `world`

Primary editorial world placement.

This is an organizational placement, not a claim of exclusive historical ownership.

### `region`

Primary editorial regional placement.

A region identifies the current editorial shelf of the manifestation.

It does not mean that the person, event, community, polity, source, or phenomenon belongs only to that region.

### `hub`

Primary editorial hub placement.

A hub provides a current organizational context.

It does not prevent the same identity from being linked from other hubs, regions, themes, timelines, or research questions.

### `period`

A broad historical period label.

Period metadata should not replace discussion of chronology in the article body.

### `date_start` and `date_end`

Approximate chronological values for filtering, timelines, and machine-readable use.

When chronology is uncertain, that uncertainty belongs in the body.

### `related`

A manually reviewed list of strongly related `entry_key` values.

This field should not substitute for future navigation or relationship infrastructure.

### `claim_status`

A high-level guide to the evidentiary condition of the article.

Possible values include:

- `stable`
- `mixed`
- `contested`
- `hypothesis_heavy`
- `source_limited`

This field is only a signal.

It does not replace direct reading of the relevant claims, evidence, uncertainties, and source discussion.

### `license`

License information for original sanapedia content or page-specific reuse conditions.

Repository-level defaults may be inherited where appropriate.

---

## 5. Metadata and article-body responsibilities

Frontmatter supports identity, classification, publication, navigation, retrieval, revision tracking, and machine-readable use.

Frontmatter must not become a substitute for historical reasoning.

The article body is responsible for preserving substantive historical content, including where relevant:

- historical claims;
- evidence;
- source distance;
- source limitations;
- chronology;
- uncertainty;
- contemporary perceptions;
- surviving records;
- interpretation;
- competing interpretations;
- hypotheses;
- unknowns.

Metadata may summarize or signal these conditions.

It must not flatten them.

---

## 6. Durable identity and editorial placement

sanapedia separates durable identity from editorial placement.

The `entry_key` is identity.

The following are not identity:

- title;
- preferred name;
- slug;
- URL;
- file path;
- language;
- world;
- region;
- hub;
- entity type;
- publication status.

Physical file placement exists for research, writing, translation, maintenance, and publication organization.

It does not establish exclusive historical ownership.

A single identity may be relevant to multiple regions, historical hubs, themes, periods, communities, or research questions.

Current file placement records the present editorial organization only.

If a manifestation moves to another path, the durable identity remains unchanged.

---

## 7. Generated publication fields

Public URLs and related publication data should normally be generated from Registry v2, file placement, frontmatter, and publication rules.

Examples include:

- HTML URL;
- canonical Markdown URL;
- canonical HTML URL;
- language alternates;
- sitemap URL;
- catalog records.

These values should not normally be duplicated manually in every Markdown file.

Manual URL metadata creates unnecessary breakage when publication structure changes.

The stable source layer consists of:

- `entry_key`;
- language;
- Registry v2 mapping;
- repository file path;
- frontmatter;
- canonical Markdown content.

Publication outputs may be reconstructed from that layer.

---

## 8. Revision boundary

This specification defines the presence and meaning of metadata such as:

- `revision`;
- `updated`;
- `status`;
- `entry_key`.

It does not define the full practice for citing earlier revisions, preserving transformation provenance, handling superseded material, or representing downstream summaries and translations.

Those responsibilities belong to the Revision and Citation Policy.

---

## 9. Relationship to other documents

This specification should be read together with:

- Registry v2 Specification — durable identity and manifestation mapping;
- Revision and Citation Policy — revision continuity, citation, transformation, and provenance;
- SANA Historical Reading Protocol — historical reading and analytical practice;
- Source Trifurcation — Fact, Perception, and Record;
- Three-Layer Analysis — Survival, Narrative, and Institution.

Together, these documents separate:

- identity;
- metadata;
- publication;
- historical evidence;
- interpretation;
- analytical method;
- revision and citation practice.

That separation is intentional.

sanapedia should remain reconstructible even when names, URLs, interfaces, publication systems, or editorial organization change.
