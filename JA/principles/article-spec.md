---
entry_key: "sp_00000051"
title: "記事仕様"
slug: "article-spec"
entity_type: "policy"
content_type: "policy"
status: "provisional"
revision: "0.2"
language: "ja"
published: "2026-09-13"
updated: "2026-10-02"
---

# 記事仕様

## 1. 目的

この文書は、公開されるsanapedia知識ページの構造要件を定義する。

本仕様は、以下を支えるために存在する。

- 永続的なentry identity
- 言語ごとのmanifestation
- revision管理
- 引用
- canonical Markdownへのアクセス
- 公開
- machine-readable catalog
- AIおよびretrievalでの利用
- editorial validation

この仕様が定義するのは、ページ構造とmetadataの責務である。

歴史分析そのものを置き換えるものではない。

歴史上の主張、証拠、解釈、不確実性、史料上の制約、競合する解釈、仮説は記事本文に置く。

---

## 2. 基本原則

登録された公開knowledge pageは、以下を持たなければならない。

1. 永続的な `entry_key`
2. 言語ごとのMarkdown manifestation
3. 有効なfrontmatter
4. `entity_type` と `content_type` に適した記事内容
5. identity・language・file pathを結ぶRegistry v2 mapping

Markdownファイルは、永続的なknowledge sourceである。

HTMLページ、index、navigation、catalog、sitemap、その他の公開出力は、そこから生成されるprojectionである。

---

## 3. 必須metadata

すべての公開・登録済みmanifestationは、以下のfrontmatter fieldを持たなければならない。

### `entry_key`

research entryの永続的なidentity。

規則:

- 必須
- quoted string
- 形式は `sp_00000000`
- Registry v2と一致しなければならない
- 再利用してはならない
- language、geography、period、hierarchy、status、entity typeを埋め込んではならない
- 同一research identityのすべてのlanguage manifestationは、同じ `entry_key` を共有する

title、slug、URL、file location、editorial placement、本文表現が変わっても、新しいidentityにはならない。

### `title`

そのlanguage manifestationにおける表示title。

規則:

- 必須
- quoted string
- language-specific
- 将来変更してよい
- identityを決定しない

### `language`

manifestationの言語。

規則:

- 必須
- lowercase
- quoted string
- Registry v2のmanifestation mappingおよびlanguage rootと一致しなければならない

schemaは固定のlanguage setを要求しない。

### `status`

entryのlifecycleまたはeditorial state。

許可値:

- `draft`
- `active`
- `provisional`
- `superseded`
- `redirected`
- `withdrawn`

statusは `entry_key` を変更せずに変化してよい。

withdrawn、redirected、supersededとなったidentityを、identity registryから黙って削除したり再利用したりしてはならない。

### `entity_type`

entryが表すentityまたはconceptual objectの種類を示す。

許可値:

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

editorial understandingの変化によって `entity_type` が変わることはあり得る。

その変更はidentityを変更しない。

### `content_type`

そのページがsanapedia内でどのような機能を持つかを示す。

許可値:

- `historical_entry`
- `historical_hub`
- `timeline`
- `policy`
- `principle`
- `index`
- `source_note`
- `column`

`entity_type` と `content_type` は関連するが、同一ではない。

例:

```yaml
entity_type: "event"
content_type: "historical_entry"
```

前者はentryが何についてのものかを示す。

後者はページがどのように機能するかを示す。

### `revision`

そのlanguage manifestationにおける可視のrevision number。

規則:

- 必須
- quoted string
- language manifestationごとに異なってよい
- substantive contentが変わった場合は上げる
- identityを決定しない

初期値の例:

```text
0.1
0.2
0.3
1.0
1.1
```

revisionの扱いとcitation practiceは、Revision and Citation Policyで別途定義する。

### `updated`

そのlanguage manifestationが最後にmaterially updatedされた日付。

規則:

- 必須
- quoted string
- ISO形式 `YYYY-MM-DD`
- language manifestationごとに異なってよい
- claim、source note、interpretation、structure、title、statusが実質的に変更された場合に更新する

---

## 4. 推奨metadata

以下のfieldはminimum schemaでは必須ではないが、該当する場合は推奨する。

### `summary`

index、search result、preview、AI catalog、navigation向けの短いlanguage-specific description。

summaryは確実性を過度に強く表現してはならない。

### `world`

主要なeditorial world placement。

これは整理上のplacementであり、排他的なhistorical ownershipを意味しない。

### `region`

主要なeditorial regional placement。

regionは、そのmanifestationの現在のeditorial shelfを示す。

person、event、community、polity、source、phenomenonが、そのregionだけに属することを意味しない。

### `hub`

主要なeditorial hub placement。

hubは、現在のorganizational contextを与える。

同じidentityが別のhub、region、theme、timeline、research questionから参照されることを妨げない。

### `period`

大まかなhistorical period label。

period metadataは、記事本文におけるchronologyの議論を置き換えない。

### `date_start` と `date_end`

filtering、timeline、machine-readable useに使う、おおよそのchronological value。

chronologyに不確実性がある場合、その不確実性は本文で説明する。

### `related`

強い関連があり、manual reviewされた `entry_key` のlist。

将来のnavigationまたはrelationship infrastructureの代替として使わない。

### `claim_status`

記事全体のevidentiary conditionを示す高レベルのguide。

候補値:

- `stable`
- `mixed`
- `contested`
- `hypothesis_heavy`
- `source_limited`

これはsignalにすぎない。

関連するclaim、evidence、uncertainty、source discussionを直接読むことの代替にはならない。

### `license`

sanapedia original contentまたはpage-specific reuse conditionに関するlicense情報。

適切な場合、repository-level defaultを継承してよい。

---

## 5. metadataと記事本文の責務

frontmatterは、identity、classification、publication、navigation、retrieval、revision tracking、machine-readable useを支える。

frontmatterをhistorical reasoningの代替にしてはならない。

記事本文は、該当する場合、以下のsubstantive historical contentを保持する責務を持つ。

- historical claim
- evidence
- source distance
- source limitation
- chronology
- uncertainty
- contemporary perception
- surviving record
- interpretation
- competing interpretation
- hypothesis
- unknown

metadataは、これらの状態を要約したりsignalとして示したりしてよい。

しかし、それらを平板化してはならない。

---

## 6. 永続identityとeditorial placement

sanapediaでは、durable identityとeditorial placementを分離する。

`entry_key` がidentityである。

以下はidentityではない。

- title
- preferred name
- slug
- URL
- file path
- language
- world
- region
- hub
- entity type
- publication status

physical file placementは、research、writing、translation、maintenance、publication organizationのために存在する。

それはexclusive historical ownershipを確定しない。

単一のidentityが、複数のregion、historical hub、theme、period、community、research questionに関係してよい。

現在のfile placementが記録するのは、その時点のeditorial organizationだけである。

manifestationが別のpathへ移動しても、durable identityは変わらない。

---

## 7. 生成されるpublication field

public URLや関連するpublication dataは、通常、Registry v2、file placement、frontmatter、publication ruleから生成する。

例:

- HTML URL
- canonical Markdown URL
- canonical HTML URL
- language alternate
- sitemap URL
- catalog record

これらを各Markdown fileへ手動で重複記載することは、通常避ける。

manual URL metadataは、publication structureが変わったときに不要な破損を生みやすい。

stable source layerを構成するのは以下である。

- `entry_key`
- language
- Registry v2 mapping
- repository file path
- frontmatter
- canonical Markdown content

publication outputは、このlayerから再構築できる。

---

## 8. revisionの責務境界

この仕様は、以下のmetadataの存在と意味を定義する。

- `revision`
- `updated`
- `status`
- `entry_key`

ただし、過去revisionのcitation、transformation provenanceの保持、superseded materialの扱い、downstream summaryやtranslationの表現方法までは定義しない。

それらはRevision and Citation Policyの責務である。

---

## 9. 他文書との関係

この仕様は、以下の文書とあわせて読む。

- Registry v2 Specification — durable identityとmanifestation mapping
- Revision and Citation Policy — revision continuity、citation、transformation、provenance
- SANA Historical Reading Protocol — historical readingとanalytical practice
- Source Trifurcation — Fact、Perception、Record
- Three-Layer Analysis — Survival、Narrative、Institution

これらの文書は共同で、以下を分離する。

- identity
- metadata
- publication
- historical evidence
- interpretation
- analytical method
- revision and citation practice

この分離は意図的なものである。

名称、URL、interface、publication system、editorial organizationが変わっても、sanapediaは再構築可能であるべきだ。
