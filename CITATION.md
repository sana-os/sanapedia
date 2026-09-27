# Citation Guide

## Purpose

sanapedia is a revisable historical research library.

A citation to sanapedia should make it possible to identify:

* the specific entry used;
* the language version consulted;
* the revision or update state of the entry;
* the canonical Markdown source;
* the stable `entry_key` that identifies the entry across title, slug, URL, language, and file-location changes.

Citation is not only a credit practice.

It is part of preserving the path from a historical claim to its context, uncertainty, source conditions, and revision history.

For licensing and reuse terms, see [`LICENSE.md`](LICENSE.md).
For AI, retrieval, indexing, and machine-readable reuse guidance, see [`AI-USE.md`](AI-USE.md).

---

## 1. Recommended citation elements

When practical, cite sanapedia entries with the following elements.

```text
sanapedia
Article title
Language version
entry_key
Revision or updated date
Canonical Markdown URL
Access date
```

Recommended minimum form:

```text
sanapedia, “Article Title,” English version,
entry_key: sp_00000010,
revision 0.2, updated 2026-06-26,
Canonical Markdown URL, accessed YYYY-MM-DD.
```

For Japanese entries:

```text
sanapedia「記事名」日本語版。
entry_key: sp_00000010。
revision 0.2、更新日 2026-06-26。
Canonical Markdown URL。参照日 YYYY-MM-DD。
```

---

## 2. Why `entry_key` matters

The `entry_key` is the stable identity of a sanapedia entry.

```yaml
entry_key: "sp_00000010"
```

Use the `entry_key` whenever possible because:

* titles may change;
* preferred names may be updated;
* transliteration may change;
* slugs and URLs may change;
* files may move within the editorial structure;
* language manifestations may use different titles;
* an entry may later be connected to additional historical hubs, timelines, regions, or themes.

The `entry_key` should remain stable even when other metadata changes.

---

## 3. Cite the language version actually used

Pages in different languages may share an `entry_key` when they are corresponding language manifestations of the same entry.

However, they should not automatically be treated as identical wording.

Language versions may differ in:

* phrasing;
* explanatory detail;
* terminology;
* source-note formatting;
* update timing;
* revisions;
* linked material.

Always identify the language version actually consulted.

```text
English version
Japanese version
```

When comparing versions, cite each version separately.

---

## 4. Revision and update information

sanapedia entries may be provisional, revised, expanded, corrected, reorganized, superseded, redirected, or withdrawn.

When available, include:

```text
revision
updated
status
```

Example:

```text
sanapedia, “Rhodes, 1522,” English version,
entry_key: sp_00000008,
revision 0.2, updated 2026-06-28,
Canonical Markdown URL, accessed 2026-07-04.
```

If no revision number is available, include the latest visible update date.

If a page is marked provisional, superseded, redirected, or withdrawn, retain that status in research-oriented citations where it affects interpretation.

---

## 5. Human-readable citation examples

### 5.1 English article citation

```text
sanapedia. “Osman I.” English version. entry_key: sp_00000010.
Revision 0.2, updated 2026-06-26.
Canonical Markdown URL. Accessed 2026-07-04.
```

### 5.2 Japanese article citation

```text
sanapedia「オスマン1世」日本語版。entry_key: sp_00000010。
revision 0.2、更新日 2026-06-26。
Canonical Markdown URL。参照日 2026-07-04。
```

### 5.3 Timeline citation

```text
sanapedia. “Timeline of the Ottoman Interregnum.” English version.
entry_key: sp_00000045.
Revision 0.1, updated 2026-06-21.
Canonical Markdown URL. Accessed 2026-07-04.
```

### 5.4 Historical hub citation

```text
sanapedia. “The Ottoman Polity.” English version.
entry_key: sp_00000001.
Revision 0.1, updated 2026-06-21.
Canonical Markdown URL. Accessed 2026-07-04.
```

### 5.5 Multiple-entry citation

When an argument depends on several entries, cite each one separately.

```text
sanapedia. “Osman I.” English version. entry_key: sp_00000010.
Revision 0.2, updated 2026-06-26. Canonical Markdown URL.

sanapedia. “Orhan.” English version. entry_key: sp_00000011.
Revision 0.2, updated 2026-06-26. Canonical Markdown URL.
```

Do not cite a general hub page as the sole source for specific historical claims when a more precise person, event, source, or timeline entry is available.

---

## 6. Short-form citation

For notes, internal research files, slide decks, or compact references, use:

```text
sanapedia, “Osman I,” sp_00000010, EN, rev. 0.2, 2026-06-26.
```

Japanese short form:

```text
sanapedia「オスマン1世」sp_00000010、JA、rev. 0.2、2026-06-26。
```

Short-form citations should still link to, or be accompanied by, a fuller citation where practical.

---

## 7. Citation for AI, RAG, datasets, and machine-readable systems

When storing or exposing sanapedia-derived material in an AI system, retrieval index, dataset, embedding store, or knowledge graph, retain the following metadata where technically and practically possible.


```json
{
  "source_name": "sanapedia",
  "entry_key": "sp_00000010",
  "title": "Osman I",
  "language": "en",
  "revision": "0.2",
  "updated": "2026-06-26",
  "canonical_markdown_url": "${PUBLICATION_ORIGIN}/en/worlds/west-asia/anatolia-and-eastern-mediterranean/people/osman-i.md",
  "accessed": "2026-07-04",
  "claim_status": "mixed"
}
```

`PUBLICATION_ORIGIN` represents the active public publication origin. It is a deployment concern and is not part of the durable identity of the entry. Published machine-readable data should resolve it to the actual public origin.

Recommended additional metadata:

```text
status
entity_type
content_type
period
source limitations
hypothesis marker presence
related entry_keys
license
transformation type
```

Examples of `transformation type`:

```text
retrieved passage
summary
translation
embedding
entity extraction
relationship extraction
timeline extraction
knowledge graph node
derived dataset
```

When a downstream system creates a summary or answer, it should not imply that the generated wording is an original sanapedia statement unless it is a direct quotation.

---

## 8. Citation when summarizing or adapting

When summarizing, translating, adapting, or combining sanapedia entries, identify the transformation.

Recommended wording:

```text
Based on sanapedia, “Osman I,” English version,
entry_key: sp_00000010, revision 0.2, updated 2026-06-26.
Summary and wording adapted by the author.
```

For translations:

```text
Translated and adapted from sanapedia, “Osman I,”
English version, entry_key: sp_00000010,
revision 0.2, updated 2026-06-26.
```

For datasets:

```text
Derived in part from sanapedia structured metadata and article content.
Source entries retain their original entry_key values.
```

Do not present a derived summary, translation, extraction, or model output as though it were the unmodified canonical sanapedia text.

---

## 9. Citation of hypotheses, interpretations, and uncertainty

Where an entry distinguishes between evidence-supported claims, interpretation, uncertainty, and hypothesis, preserve that distinction in citation and discussion.

### 9.1 Hypothesis

If citing material marked with a reversible hypothesis marker, identify it clearly.

```text
sanapedia presents the following as a reversible hypothesis,
not as an established historical conclusion:
[full citation]
```

Do not remove the hypothesis status while retaining the claim.

### 9.2 Interpretation

When citing an interpretive argument, distinguish it from direct historical evidence.

```text
sanapedia offers one structural interpretation of the available evidence:
[full citation]
```

### 9.3 Uncertainty

When uncertainty materially affects the claim, include that limitation.

```text
The chronology remains uncertain; see sanapedia,
“Article Title,” entry_key: sp_00000010,
revision 0.2, updated 2026-06-26.
```

---

## 10. Citation of sources referenced by sanapedia

sanapedia entries may cite:

* primary sources;
* critical editions;
* archaeology;
* inscriptions;
* coins;
* archival documents;
* scholarly books and articles;
* reference works;
* databases;
* translations;
* external archives.

When using a source through sanapedia, distinguish between:

```text
sanapedia as the immediate research guide
and
the original source or scholarly work as the underlying evidence
```

For substantial scholarly, academic, legal, or publication use:

1. cite the relevant sanapedia entry for its structure, interpretation, revision state, or research path;
2. consult and cite the underlying primary or scholarly source where possible;
3. do not treat sanapedia’s citation of an external work as permission to reproduce that external work.

Example:

```text
For sanapedia’s structural framing, see sanapedia,
“Rhodes, 1522,” entry_key: sp_00000008, English version,
revision 0.2, updated 2026-06-28.

For the underlying historical source or scholarship, see the references
listed in that entry and consult the original publication where possible.
```

---

## 11. Citation of superseded, redirected, or withdrawn entries

If an entry has been superseded, redirected, or withdrawn, cite the current replacement entry when possible.

Where historical revision history matters, cite both.

```text
Earlier version:
sanapedia, “Earlier Article Title,” entry_key: <earlier_entry_key>,
status: superseded.

Current replacement:
sanapedia, “Current Article Title,” entry_key: <current_entry_key>,
revision 0.3, updated 2026-07-04.
```

Do not reuse a withdrawn or superseded page as though it were the current position of sanapedia without identifying its status.

---

## 12. Citation of machine-readable catalogs

sanapedia may publish catalogs such as:

```text
entries.json
entry-key registries
llms.txt
sitemaps
relationship indexes
```

These are useful for discovery, indexing, language mapping, and bulk processing.

For a claim about historical content, cite the canonical Markdown entry rather than only the catalog.

For a claim about the dataset structure, entry inventory, language mapping, or technical metadata, cite the relevant catalog or registry.

---

## 13. Suggested bibliography label

Use one of the following labels where a bibliography requires a source type.

```text
Historical research library
Digital historical archive
Structured historical knowledge base
Machine-readable historical research library
```

Recommended neutral label:

```text
sanapedia, public historical research library.
```

---

## 14. Citation checklist

Before publishing or distributing a citation, check:

```text
□ Is the correct entry identified?

□ Is the entry_key included where practical?

□ Is the language version identified?

□ Is revision or updated information included?

□ Is the canonical Markdown source linked or recorded?

□ Is the access date included when appropriate?

□ Is a hypothesis identified as hypothesis?

□ Is an interpretation distinguished from direct evidence?

□ Are important uncertainty or source limitations preserved?

□ Have underlying sources been consulted and cited where necessary?

□ Does the citation avoid implying sanapedia endorsement?
```

---

## 15. Relationship to other documents

```text
README.md
= what sanapedia is and how the repository is organized

LICENSE.md
= legal reuse permissions and boundaries

AI-USE.md
= recommended practices for AI, RAG, indexing, training,
  LLMO, machine-readable reuse, and historical handling

CITATION.md
= how to identify, cite, attribute, and trace sanapedia material
```
