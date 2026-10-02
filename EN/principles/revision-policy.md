---
entry_key: "sp_00000052"
title: "Revision and Citation Policy"
slug: "revision-policy"
entity_type: "policy"
content_type: "policy"
status: "provisional"
revision: "0.2"
language: "en"
published: "2026-09-13"
updated: "2026-10-02"
---

# Revision and Citation Policy

## 1. Purpose

sanapedia is a revisable historical research library.

Revision is not treated as a defect to be hidden.

A revised page should remain traceable to the durable research identity, language manifestation, revision state, source conditions, and interpretive context from which it developed.

This policy defines how sanapedia preserves continuity across revision and how sanapedia material should be cited, transformed, reused, and referenced.

Its purpose is to prevent revision from erasing provenance and to prevent citation from flattening uncertainty, interpretation, or source conditions.

---

## 2. Durable identity across revision

The `entry_key` is the durable identity of an entry.

It remains stable when any of the following change:

- title;
- preferred name;
- transliteration;
- slug;
- URL;
- repository file path;
- editorial placement;
- wording;
- structure;
- language-specific revision;
- publication status.

A substantive revision does not normally create a new identity.

The revision belongs to the manifestation.

The identity persists across revisions unless the editorial decision is that the material represents a genuinely different research object requiring a new `entry_key`.

Existing `entry_key` values must not be silently reused for unrelated material.

---

## 3. Language manifestations and revision state

Language manifestations may share the same `entry_key` while differing in wording, terminology, explanatory detail, source-note formatting, update timing, and revision number.

Corresponding language versions should therefore not be assumed to be textually identical.

Each manifestation maintains its own:

- `language`;
- `revision`;
- `updated`;
- visible wording;
- language-specific editorial state.

When citing or reusing sanapedia material, identify the language manifestation actually consulted.

When comparing language manifestations, cite each one separately.

A revision to the English canonical editorial baseline does not automatically change the revision number of another language manifestation.

Other manifestations may be updated later and may therefore temporarily differ in revision state.

---

## 4. What a citation should preserve

Where practical, a citation to a sanapedia entry should preserve enough information to identify the exact research object and manifestation used.

Recommended elements are:

- sanapedia;
- article title;
- language version;
- `entry_key`;
- revision;
- updated date;
- status where relevant;
- canonical Markdown URL;
- access date.

A compact citation may omit some elements where necessary, but `entry_key`, language, and revision or updated state should be retained where practical.

The purpose of this information is not only attribution.

It preserves the path from a historical claim back to its context, revision state, uncertainty, source limitations, and editorial history.

---

## 5. Canonical Markdown and publication projections

Markdown is the durable canonical content source for sanapedia entries.

Public HTML pages, navigation pages, indexes, machine-readable catalogs, sitemaps, and other interfaces are publication projections.

Where practical, citation should identify the canonical Markdown source in addition to or instead of a presentation-layer URL.

A change in publication system, domain, route, or interface does not change the durable identity of the entry.

The citation model should therefore prefer durable identity and canonical source information over interface-specific structure.

---

## 6. Revision, updated date, and status

The following fields describe the visible state of a language manifestation:

- `revision`;
- `updated`;
- `status`.

`revision` identifies a visible version state of the manifestation.

`updated` records the date of the most recent material change to that manifestation.

`status` records the lifecycle or editorial state of the entry.

Relevant status values include:

- `draft`;
- `active`;
- `provisional`;
- `superseded`;
- `redirected`;
- `withdrawn`.

Where status materially affects interpretation or reuse, it should be preserved in citation and downstream metadata.

A provisional page should not silently become equivalent to a stable one through downstream transformation.

A superseded or withdrawn page should not lose that state merely because its text remains accessible.

---

## 7. Transformation provenance

sanapedia material may be transformed for research, publication, AI, retrieval, or structured-data use.

Examples include:

- retrieved passage;
- summary;
- translation;
- adaptation;
- embedding;
- entity extraction;
- relationship extraction;
- timeline extraction;
- knowledge graph node;
- derived dataset;
- model-generated answer.

When material has been transformed, the transformation should be identified where technically and practically possible.

Derived material must not be presented as though it were unchanged canonical sanapedia text.

For example, a downstream summary should identify that it is a summary.

A translation should identify the source manifestation and that translation has occurred.

A dataset should preserve source `entry_key` values where possible.

The purpose of transformation provenance is to keep the path from derived output back to the source manifestation visible.

---

## 8. Preserve epistemic status

sanapedia distinguishes among evidence-supported claims, interpretation, uncertainty, hypothesis, and unknowns.

Citation and transformation should preserve those distinctions.

### 8.1 Evidence-supported claims

A claim presented as supported by available evidence may be summarized or reused, but its evidentiary context should not be strengthened beyond what the source supports.

### 8.2 Interpretation

An interpretive argument must not be transformed into the appearance of direct historical evidence.

If sanapedia offers a structural interpretation of available evidence, downstream use should preserve that interpretive status.

### 8.3 Uncertainty

Where uncertainty materially affects a claim, the uncertainty should remain visible.

A citation or summary should not convert an uncertain chronology, disputed identification, or incomplete source record into an unqualified statement.

### 8.4 Hypothesis

A reversible hypothesis must remain identifiable as a hypothesis.

Removing the hypothesis marker while retaining the claim changes its epistemic status and is therefore not a faithful transformation.

### 8.5 Unknowns

Where the source explicitly preserves an unknown, downstream systems should not silently replace that unknown with unsupported certainty.

---

## 9. Lifecycle states and historical continuity

sanapedia preserves identity history across lifecycle changes.

Entries may become:

- provisional;
- superseded;
- redirected;
- withdrawn.

These states do not erase the identity.

Where technically and editorially appropriate, historical mappings and lifecycle information should remain recoverable.

A superseded entry may remain useful for understanding earlier research states.

A redirected entry may continue to preserve identity continuity.

A withdrawn entry should not be silently reused for a different research object.

Revision history is part of research provenance.

---

## 10. sanapedia citation and underlying historical sources

sanapedia may be cited as:

- a research guide;
- a structured historical synthesis;
- a methodological interpretation;
- an editorial knowledge source;
- a machine-readable research resource.

However, citing sanapedia is not always equivalent to citing the underlying historical source on which a claim depends.

Where a specific primary source, scholarly edition, archival record, inscription, chronicle, dataset, or secondary work is the evidentiary basis of a claim, users should cite that underlying source directly when appropriate.

sanapedia citation identifies the research layer that organized, interpreted, or presented the material.

Underlying-source citation identifies the evidence or scholarship on which the claim rests.

These functions should not be conflated.

---

## 11. Precision and multiple-entry citation

When a claim depends on a specific person, event, source, timeline, or other entry, cite the most precise relevant entry where practical.

A broad hub should not normally be used as the sole citation for a precise claim when a more specific entry exists.

When an argument depends on several sanapedia entries, cite each relevant entry separately rather than collapsing them into one general citation.

This preserves the mapping between individual claims and their supporting research objects.

---

## 12. Machine-readable reuse

When sanapedia-derived material is stored or exposed in an AI system, retrieval index, dataset, embedding store, knowledge graph, or other machine-readable environment, retain the following where technically and practically possible:

- source name;
- `entry_key`;
- title;
- language;
- revision;
- updated;
- status;
- canonical Markdown URL;
- access date;
- transformation type.

Recommended additional metadata may include:

- `entity_type`;
- `content_type`;
- `claim_status`;
- period;
- source limitations;
- hypothesis-marker presence;
- related `entry_key` values;
- license information.

Machine-readable reuse should preserve provenance without implying that transformed or generated wording is canonical sanapedia text.

---

## 13. Relationship to Article Specification

Article Specification defines what metadata a sanapedia page carries and what responsibilities belong to the article body.

This policy defines how that information should remain traceable when the page changes, is cited, or is transformed.

In particular:

- Article Specification defines `entry_key`, `revision`, `updated`, and `status`;
- Revision and Citation Policy defines how those fields support continuity and citation;
- Article Specification defines the boundary between metadata and historical analysis;
- Revision and Citation Policy defines how that boundary should survive reuse and transformation.

The two documents are complementary.

---

## 14. Relationship to methodology

This policy should also be read together with:

- Registry v2 Specification — durable identity and manifestation mapping;
- SANA Historical Reading Protocol — historical reading and analytical practice;
- Source Trifurcation — Fact, Perception, and Record;
- Three-Layer Analysis — Survival, Narrative, and Institution.

These documents operate at different layers.

Registry v2 preserves identity and manifestation mapping.

Article Specification defines page structure.

Revision and Citation Policy preserves continuity and provenance.

The methodological documents define how historical material is observed and interpreted.

Keeping these responsibilities separate helps sanapedia remain traceable even when content, languages, URLs, publication systems, or editorial structures change.
