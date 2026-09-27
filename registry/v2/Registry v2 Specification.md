# Pastfold Registry v2 Specification

## Status

**Current registry authority.**

Registry v2 separates durable entry identity from language-specific
manifestations.

The authoritative registry files are:

```text
registry/v2/entry-registry.csv
registry/v2/entry-language-registry.csv
```

Registry v1 is retained as a frozen legacy record for provenance,
migration history, and reproducibility.

---

## 1. Purpose

Registry v2 separates two concepts:

1. durable historical entry identity;
2. language-specific manifestations of that identity.

The registry is not the public article catalog.

It is the editorial identity and mapping layer from which validation,
machine-readable catalogs, language relationships, and publication
routing can be derived.

---

## 2. Authoritative files

### `entry-registry.csv`

Schema:

```csv
entry_key,status,notes
```

Authority for:

```text
entry_key existence
entry_key reuse prevention
identity lifecycle status
identity-level editorial notes
withdrawn / redirected / superseded identity preservation
```

Example:

```csv
sp_00000010,active,
```

### `entry-language-registry.csv`

Schema:

```csv
entry_key,language,file
```

Authority for:

```text
language manifestation existence
entry_key + language mapping
repository file mapping
```

Example:

```csv
sp_00000010,en,EN/worlds/west-asia/anatolia-and-eastern-mediterranean/people/osman-i.md
sp_00000010,ja,JA/worlds/west-asia/anatolia-and-eastern-mediterranean/people/osman-i.md
```

---

## 3. Durable identity

`entry_key` is the durable technical identity of a Pastfold knowledge unit.

Format:

```text
sp_00000000
```

Validation pattern:

```regex
^sp_[0-9]{8}$
```

The key is opaque and immutable.

It MUST NOT encode:

```text
language
geography
period
dynasty
polity
entity type
publication status
hierarchy
URL
file location
```

An `entry_key` is never reused.

Changes to title, preferred name, slug, URL, language availability,
repository path, classification, or public brand do not change it.

---

## 4. Language manifestations

One identity may have zero, one, two, or many language manifestations.

Conceptually:

```text
entry_key
├─ en
├─ ja
├─ tr
├─ ar
├─ zh-hant
└─ ...
```

There is **no required language set**.

English and Japanese are the languages present in the initial Registry v2
migration. They are not structurally privileged.

Valid configurations may include:

```text
en only
ja only
tr only
en + ja
ja + tr
en + ja + ar + fr
many languages
```

Applications must discover language availability from
`entry-language-registry.csv`.

They must not assume that every identity has English, Japanese, or any
other specific language.

---

## 5. Language tags

The `language` column uses normalized lowercase language tags suitable for
stable machine processing and public routing.

Examples:

```text
en
ja
tr
ar
fr
de
zh-hant
pt-br
```

Language is metadata associated with a manifestation.

Language is not identity.

Adding or removing a language manifestation does not change `entry_key`.

---

## 6. Manifestation uniqueness

The pair:

```text
(entry_key, language)
```

must be unique.

Under the current canonical-source model, an identity has at most one
current Markdown manifestation for a given language.

A repository file must not be mapped as the current manifestation of more
than one `(entry_key, language)` pair.

---

## 7. Repository paths

The `file` column stores a repository-relative POSIX path.

Correct:

```text
EN/worlds/west-asia/anatolia-and-eastern-mediterranean/people/osman-i.md
```

Do not store:

```text
/home/user/sanapedia/EN/...
sanapedia\EN\...
C:\...
```

Rules:

```text
relative to repository root
forward slashes
no leading slash
no ..
no repository-name prefix
```

Repository paths describe source organization.

They are not canonical public URLs and are not durable identity.

---

## 8. Frontmatter agreement

Every current mapped manifestation must agree with Registry v2.

At minimum:

```text
frontmatter.entry_key == registry entry_key
frontmatter.language  == registry language
```

Markdown frontmatter remains the article-level source for fields such as:

```text
title
language
status
entity_type
content_type
revision
updated
summary
period
claim_status
slug
```

Registry v2 should not duplicate article-level metadata without a later
structural reason.

---

## 9. Zero-manifestation identities

Identity preservation and current publication are separate concerns.

An identity may remain in `entry-registry.csv` even when it has no current
language manifestation.

This allows Pastfold to preserve lifecycle history and prevent identifier
reuse for identities whose content has been:

```text
withdrawn
redirected
superseded
```

Publication tooling may impose stricter rules for identities intended for
current publication.

The identity registry itself must not require an identity to disappear
merely because its current files disappear.

---

## 10. Public URLs are generated

Registry v2 does not store:

```text
html_url
canonical_html_url
canonical_markdown_url
language_alternates
sitemap_url
```

These are generated from:

```text
Registry v2
+ Markdown frontmatter
+ repository mapping
+ publication configuration
+ public URL rules
```

A URL is an address, not identity.

The durable identity remains `entry_key`.

---

## 11. Language relationships

Pastfold does not require `translation_of` to relate manifestations of the
same entry.

Language manifestations are related through their shared `entry_key`.

They may differ in:

```text
revision
updated date
article status
wording
local editorial development
```

They still represent manifestations of the same durable knowledge identity.

Generated `language_alternates` should enumerate the manifestations that
currently exist for that `entry_key`.

---

## 12. Classification and routing

Geographic, dynastic, political, cultural, and chronological classifications
must not be encoded into `entry_key`.

Public routing may use geographic namespaces for discovery.

Such routes are projections over the durable identity layer.

The same entry may be discoverable from multiple historical indexes or
contexts without receiving multiple identities.

---

## 13. Deterministic ordering

`entry-registry.csv` should be ordered by:

```text
entry_key
```

`entry-language-registry.csv` should be ordered by:

```text
entry_key
language
```

Ordering carries no historical meaning.

It exists for deterministic maintenance and reproducible generation.

---

## 14. Initial migration profile

The initial Registry v2 migration contains:

```text
46 identities
92 language manifestations
en: 46
ja: 46
```

These numbers describe the current dataset.

They are **not schema constraints**.

Future validators and generators must derive counts from Registry v2.

They must not hard-code:

```text
46
92
en
ja
```

as permanent Pastfold requirements.

---

## 15. Registry v1

The former registry is retained at:

```text
registry/entry-key-registry.csv
```

Its historical specification is retained at:

```text
registry/Entry Key Registry Specification.txt
```

Registry v1 used:

```text
file_en
file_ja
```

New languages must not be added by extending that pattern with columns such
as:

```text
file_fr
file_tr
file_ar
```

New manifestations belong as additional rows in:

```text
registry/v2/entry-language-registry.csv
```

Registry v1 is retained for provenance and migration verification.

---

## 16. Source-of-truth hierarchy

```text
entry-registry.csv
    ↓
durable identity authority

entry-language-registry.csv
    ↓
language manifestation and repository mapping authority

Markdown frontmatter
    ↓
article-level metadata and content authority

publication configuration + URL rules
    ↓
public address derivation

entries.json / HTML / llms.txt / sitemap
    ↓
generated or rebuildable projection layer
```

The durable layers should be sufficient to reconstruct the projection layer.

---

## 17. Longevity principle

Pastfold is intended to remain reconstructable even if the current brand,
domain, software stack, or user interface no longer exists.

Therefore:

```text
entry_key is identity
URL is not identity
repository path is not identity
language is not identity
brand is not identity
```

---

## 18. Validation principles

A Registry v2 validator should check at minimum:

```text
□ Every entry_key matches ^sp_[0-9]{8}$.
□ No entry_key is duplicated in entry-registry.csv.
□ No retired identity key is reused.
□ Every language row refers to an existing entry_key.
□ Every (entry_key, language) pair is unique.
□ Language tags follow the normalized language-tag policy.
□ File paths are repository-relative POSIX paths.
□ File paths do not escape the repository.
□ Current mapped files exist when publication policy requires them.
□ Frontmatter entry_key matches the registry.
□ Frontmatter language matches the registry.
□ One current file is not reused by multiple manifestations.
□ Registry ordering is deterministic.
□ Validators do not assume a fixed language set.
□ Validators do not assume a permanent entry count.
```

---

## 19. Change policy

Changes to Registry v2 structure must be explicit and versioned.

Do not silently reinterpret existing columns.

If a future registry version becomes necessary:

```text
preserve the previous version
document the migration
validate equivalence where applicable
promote the new version explicitly
```

Historical registry versions are part of Pastfold's provenance record.
