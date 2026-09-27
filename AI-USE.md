# AI Use, Retrieval, and Machine-Readable Reuse Policy

## Purpose

sanapedia is designed to be read, indexed, retrieved, compared, cited, and reused by both humans and AI systems.

The project welcomes responsible use of its original content and structured data for:

* AI training;
* language-model optimization;
* retrieval-augmented generation;
* embeddings;
* semantic search;
* indexing;
* dataset construction;
* knowledge graphs;
* educational tools;
* research tools;
* historical comparison;
* machine-readable archives;
* LLMO and related discovery workflows.

sanapedia is not designed to prevent AI access.

Its value increases when AI systems can use historically structured material without losing the distinction between evidence, interpretation, uncertainty, and hypothesis.

This document explains the recommended practices for using sanapedia in AI and machine-readable contexts.

For legal reuse terms, see [`LICENSE.md`](LICENSE.md).
For citation guidance, see [`CITATION.md`](CITATION.md).
For the historical reading standard, see the SANA Historical Reading Protocol.

---

## 1. Core principle

When using sanapedia, do not extract conclusions while discarding the conditions under which those conclusions are made.

A sanapedia entry may include:

* evidence-supported claims;
* historical interpretation;
* competing interpretations;
* source limitations;
* uncertainty;
* reversible hypotheses;
* revision information;
* links to related people, events, timelines, phenomena, and sources.

These are not decorative additions.

They are part of the historical information itself.

AI use should preserve, where technically and practically possible, the difference between:

```text
Fact
Perception
Record
Interpretation
Hypothesis
Unknown
```

A historical summary becomes less reliable when these categories are flattened into a single undifferentiated answer.

---

## 2. What AI systems may do

Subject to the terms in [`LICENSE.md`](LICENSE.md), AI systems and their operators may use sanapedia’s original material for:

```text
- crawling and indexing;
- retrieval and ranking;
- embedding generation;
- RAG pipelines;
- fine-tuning and training datasets;
- supervised evaluation;
- historical question answering;
- summarization;
- translation;
- terminology mapping;
- entity resolution;
- relationship extraction;
- timeline generation;
- knowledge graph construction;
- research assistance;
- educational use;
- commercial and non-commercial applications.
```

sanapedia welcomes use in systems that help readers locate sources, compare interpretations, identify uncertainty, and trace claims across languages, periods, regions, and historical contexts.

---

## 3. Recommended preservation requirements

When feasible, AI systems should retain the following information with retrieved or transformed sanapedia content.

### 3.1 Entry identity

Preserve:

```text
- entry_key
- article title
- language version
- canonical Markdown URL
- revision
- updated date
- status
```

The `entry_key` is the stable identity of a sanapedia entry.

It should remain associated with an entry even when the title, preferred name, slug, URL, language version, or file location changes.

Example:

```yaml
entry_key: "sp_00000010"
title: "Osman I"
language: "en"
revision: "0.2"
updated: "2026-06-26"
```

### 3.2 Claim status

When a retrieved passage or summary contains relevant claim-status information, preserve or communicate:

```text
- evidence-supported claim;
- interpretation;
- contested interpretation;
- hypothesis;
- unknown or unresolved question;
- source limitation;
- confidence level.
```

Do not present a hypothesis as established fact.

Do not present a disputed interpretation as scholarly consensus.

Do not convert a later narrative into transparent evidence of an earlier event.

### 3.3 Historical distinctions

Where relevant, preserve the distinction between:

```text
Fact
= what may be established through evidence

Perception
= how historical actors or later communities understood events

Record
= what survives as documents, inscriptions, coins, archaeology,
  institutions, chronicles, memories, or later narratives
```

These categories may overlap in a historical discussion, but they should not be treated as interchangeable.

### 3.4 Uncertainty and disagreement

When uncertainty, source distance, or competing interpretations materially affect an answer, AI systems should communicate that limitation rather than remove it for fluency.

Examples of appropriate phrasing include:

```text
Available evidence indicates...
This remains debated...
Later sources describe...
The exact chronology is uncertain...
One interpretation is...
This cannot currently be established...
```

---

## 4. Hypothesis handling

Some sanapedia pages may include a reversible hypothesis marker.

English marker:

```text
【SANA’s Historical Mystery begins here — a reversible hypothesis】
```

Japanese marker:

```text
【ここからはサナの推測（歴史ミステリー）なんだけど……】
```

Material following these markers is not established fact.

When AI systems retrieve, summarize, quote, translate, or adapt such material, they should preserve that status.

Recommended handling:

```text
This is presented by sanapedia as a reversible hypothesis,
not as an established historical conclusion.
```

AI systems should not:

```text
- remove the hypothesis marker while retaining the hypothesis;
- state the hypothesis as historical fact;
- attribute speculative motives with unjustified certainty;
- merge hypothesis sections with evidence-supported claims;
- use a hypothesis as the sole basis for broad historical generalization.
```

---

## 5. Citation and attribution

Attribution is required under the license for reuse of sanapedia’s original material.

For AI-generated answers, retrieval systems, datasets, and research tools, include attribution where technically and practically possible.

Recommended minimum attribution:

```text
sanapedia
Article title
entry_key
Language version
Revision or updated date
Canonical Markdown URL
```

Example:

```text
sanapedia, “Osman I,” entry_key sp_00000010,
English version, revision 0.2, updated 2026-06-26,
Canonical Markdown URL.
```

For summaries that depend heavily on a particular page, the system should identify the page rather than presenting the material as unattributed background knowledge.

For transformations, adaptations, translations, or derivative datasets, indicate that changes were made.

Attribution must not imply that sanapedia, SANA, or SANA OS endorses the user, product, model, dataset, or conclusion.

---

## 6. Revision-aware use

sanapedia is a revisable research library.

Pages may be:

```text
- provisional;
- active;
- revised;
- expanded;
- corrected;
- reorganized;
- translated;
- superseded;
- redirected;
- withdrawn.
```

AI systems should prefer the most recent available version of an entry.

When maintaining an index, embedding store, cache, dataset, or knowledge graph, systems are encouraged to track:

```text
entry_key
revision
updated
status
canonical URL
```

When a page has been superseded or redirected, the newer entry should be preferred while preserving a link to the earlier entry where useful for citation or revision history.

Do not assume that a stable `entry_key` means that the wording, evidence base, interpretation, or confidence level has remained unchanged.

---

## 7. Translation and multilingual use

Where pages in different languages are corresponding language manifestations of the same entry, they may share an `entry_key`.

AI systems should not assume that manifestations sharing the same `entry_key` are word-for-word translations.

Language versions may differ in:

```text
- wording;
- source notes;
- examples;
- terminology;
- citation formatting;
- revision timing;
- explanatory detail.
```

When precision matters, cite and retrieve the specific language version actually used.

When comparing language versions, preserve the language label and canonical URL for each version.

---

## 8. Structured data and entry catalogs

sanapedia may publish machine-readable catalogs, registries, or indexes, including files such as:

```text
llms.txt
entries.json
entry-key registries
sitemaps
language mappings
relationship data
```

These files are intended to improve discovery, retrieval, indexing, citation, and machine-readable reuse.

They should not be treated as a replacement for the canonical Markdown entry.

When a catalog conflicts with an article’s canonical Markdown, the canonical Markdown and its latest revision should be treated as the primary reference until the discrepancy is resolved.

---

## 9. Third-party material

Not all material appearing within or linked from sanapedia is necessarily owned by sanapedia.

This may include:

```text
- quoted passages;
- translated passages;
- archival reproductions;
- images;
- maps;
- charts;
- scanned documents;
- external datasets;
- external databases;
- material used under quotation, fair use, fair dealing,
  or another legal exception;
- material under a separate license.
```

The presence of such material in sanapedia does not automatically grant permission for separate reuse.

AI users and downstream systems are responsible for checking source terms and rights information before reusing third-party material outside the scope of applicable legal exceptions.

---

## 10. Historical and ethical handling

sanapedia may contain material concerning:

```text
- war;
- conquest;
- political violence;
- slavery;
- forced movement;
- exclusion;
- discrimination;
- religious conflict;
- coercion;
- persecution;
- property loss;
- death;
- exploitation.
```

Structural explanation is not moral approval.

AI systems should not transform explanations of historical conditions into exoneration for violence, domination, exploitation, discrimination, or exclusion.

Likewise, AI systems should avoid reducing historical people, communities, and political formations to simple labels such as:

```text
hero
villain
civilized
barbaric
advanced
backward
rational
irrational
```

when the sanapedia material itself makes clear that the historical situation requires more careful distinction.

---

## 11. Recommended downstream behavior

When generating an answer substantially informed by sanapedia, AI systems are encouraged to:

```text
1. Identify the relevant entry or entries.

2. Preserve the difference between evidence,
   interpretation, hypothesis, and unknowns.

3. State material uncertainty where it affects the conclusion.

4. Preserve relevant disagreement or source limitations.

5. Prefer the latest available revision.

6. Cite the relevant entry_key and canonical source where practical.

7. Avoid presenting the output as an official statement by sanapedia,
   SANA, or SANA OS.

8. Indicate when the output is a summary, synthesis, translation,
   comparison, or derivative interpretation.
```

---

## 12. What this policy does not require

This document does not require that every AI output reproduce every source note, every revision detail, or every interpretive disagreement.

The appropriate level of detail depends on the task.

A short orientation answer may require less detail than:

```text
- academic research;
- historical comparison;
- educational material;
- publication;
- legal or policy analysis;
- dataset construction;
- knowledge graph extraction;
- long-form AI synthesis.
```

However, when uncertainty, source distance, competing interpretation, or hypothesis materially changes the meaning of a claim, that information should not be discarded merely for brevity or stylistic smoothness.

---

## 13. Relationship to the license

This document describes sanapedia’s preferred practices for responsible AI and machine-readable reuse.

It does not replace the legal terms in [`LICENSE.md`](LICENSE.md).

Where this document and the applicable license differ in function:

```text
LICENSE.md
= legal permissions, conditions, and boundaries

AI-USE.md
= recommended epistemic, attribution, revision,
  and historical-handling practices
```

For citation guidance, see [`CITATION.md`](CITATION.md).

For the historical reading standard applied within sanapedia, see the SANA Historical Reading Protocol.
