---
entry_key: "sp_00000052"
title: "改訂・引用ポリシー"
slug: "revision-policy"
entity_type: "policy"
content_type: "policy"
status: "provisional"
revision: "0.1"
language: "ja"
published: "2026-09-13"
updated: "2026-09-13"
---

# 改訂・引用ポリシー

## 1. 目的

Pastfoldは、改訂され続ける歴史研究ライブラリである。

改訂は、隠すべき欠陥として扱わない。

ページが改訂されても、その内容がどの永続的research identity、language manifestation、revision state、source condition、interpretive contextから発展したのかを追跡できる状態を保つべきである。

このポリシーは、Pastfoldがrevisionをまたいでcontinuityをどのように保持するか、またPastfold materialをどのように引用・変換・再利用・参照すべきかを定義する。

目的は、revisionによってprovenanceが消えることを防ぎ、citationによってuncertainty、interpretation、source conditionが平板化されることを防ぐことにある。

---

## 2. revisionをまたぐ永続identity

`entry_key` はentryのdurable identityである。

以下が変更されても、`entry_key` は維持される。

- title
- preferred name
- transliteration
- slug
- URL
- repository file path
- editorial placement
- wording
- structure
- language-specific revision
- publication status

substantive revisionは、通常、新しいidentityを作らない。

revisionはmanifestationに属する。

identityはrevisionをまたいで維持される。ただし、editorial decisionとして、それが実質的に異なるresearch objectを表すと判断された場合は、新しい `entry_key` が必要になる。

既存の `entry_key` を、無関係なmaterialのために黙って再利用してはならない。

---

## 3. language manifestationとrevision state

language manifestationは、同じ `entry_key` を共有しながら、wording、terminology、explanatory detail、source-note formatting、update timing、revision numberが異なってよい。

したがって、対応するlanguage versionをtextually identicalだと自動的にみなしてはならない。

各manifestationは、それぞれ独立して以下を持つ。

- `language`
- `revision`
- `updated`
- visible wording
- language-specific editorial state

Pastfold materialを引用または再利用するときは、実際に参照したlanguage manifestationを特定する。

複数のlanguage manifestationを比較する場合、それぞれを個別に引用する。

English canonical editorial baselineが改訂されても、他言語manifestationのrevision numberが自動的に変わるわけではない。

他言語manifestationは後から更新されてもよく、そのため一時的にrevision stateが異なることがある。

---

## 4. citationで保持すべき情報

Pastfold entryを引用するときは、可能な範囲で、使用したresearch objectとmanifestationを特定できるだけの情報を保持する。

推奨要素:

- Pastfold
- article title
- language version
- `entry_key`
- revision
- updated date
- 必要に応じてstatus
- canonical Markdown URL
- access date

簡略citationでは一部を省略してよいが、可能な範囲で `entry_key`、language、revisionまたはupdated stateを保持する。

これらの情報の目的は、単なるattributionではない。

historical claimから、そのcontext、revision state、uncertainty、source limitation、editorial historyまで遡れる経路を保持することにある。

---

## 5. canonical Markdownとpublication projection

Markdownは、Pastfold entryのdurable canonical content sourceである。

public HTML page、navigation page、index、machine-readable catalog、sitemap、その他のinterfaceはpublication projectionである。

可能な場合、citationではpresentation-layer URLだけでなく、canonical Markdown sourceを特定する。

publication system、domain、route、interfaceが変わっても、entryのdurable identityは変わらない。

そのためcitation modelでは、interface-specific structureよりも、durable identityとcanonical source informationを優先する。

---

## 6. revision・updated・status

以下のfieldは、language manifestationのvisible stateを表す。

- `revision`
- `updated`
- `status`

`revision` は、そのmanifestationの可視なversion stateを示す。

`updated` は、そのmanifestationにmaterial changeが最後に加えられた日付を記録する。

`status` は、entryのlifecycleまたはeditorial stateを記録する。

関連するstatus value:

- `draft`
- `active`
- `provisional`
- `superseded`
- `redirected`
- `withdrawn`

statusがinterpretationやreuseに実質的な影響を与える場合、そのstatusをcitationやdownstream metadataに保持する。

provisional pageがdownstream transformationによって、黙ってstable pageと同等に扱われてはならない。

supersededまたはwithdrawn pageも、textが引き続きaccess可能だからという理由だけで、そのstateを失ってはならない。

---

## 7. transformation provenance

Pastfold materialは、research、publication、AI、retrieval、structured-data useのために変換されることがある。

例:

- retrieved passage
- summary
- translation
- adaptation
- embedding
- entity extraction
- relationship extraction
- timeline extraction
- knowledge graph node
- derived dataset
- model-generated answer

materialが変換された場合、技術的・実務的に可能な範囲で、そのtransformationを明示する。

derived materialを、変更されていないcanonical Pastfold textであるかのように提示してはならない。

たとえばdownstream summaryなら、summaryであることを示す。

translationなら、source manifestationとtranslationが行われたことを示す。

datasetでは、可能な範囲でsource `entry_key` を保持する。

transformation provenanceの目的は、derived outputからsource manifestationまで戻れる経路を可視のまま保つことにある。

---

## 8. epistemic statusを保持する

Pastfoldは、evidence-supported claim、interpretation、uncertainty、hypothesis、unknownを区別する。

citationとtransformationは、その区別を保持しなければならない。

### 8.1 Evidence-supported claim

利用可能なevidenceによって支持されているclaimは、summaryやreuseが可能である。

ただし、そのevidentiary contextをsourceが支持する以上に強めてはならない。

### 8.2 Interpretation

interpretive argumentを、direct historical evidenceであるかのように変換してはならない。

Pastfoldがavailable evidenceに対するstructural interpretationを提示している場合、downstream useでもそのinterpretive statusを保持する。

### 8.3 Uncertainty

uncertaintyがclaimに実質的な影響を与える場合、そのuncertaintyは可視のままにする。

uncertain chronology、disputed identification、不完全なsource recordを、citationやsummaryによって無条件の断定に変えてはならない。

### 8.4 Hypothesis

reversible hypothesisは、hypothesisとして識別可能な状態を保たなければならない。

claimを残したままhypothesis markerだけを取り除くことは、そのepistemic statusを変更するため、faithful transformationではない。

### 8.5 Unknown

sourceが明示的にunknownを保持している場合、downstream systemはそのunknownをunsupported certaintyで黙って置き換えてはならない。

---

## 9. lifecycle stateと歴史的continuity

Pastfoldは、lifecycle changeをまたいでidentity historyを保持する。

entryは以下のstateになり得る。

- provisional
- superseded
- redirected
- withdrawn

これらのstateはidentityを消去しない。

技術的・editorialに適切な範囲で、過去のmappingとlifecycle informationを復元可能な形で保持する。

superseded entryは、過去のresearch stateを理解するために引き続き有用であり得る。

redirected entryは、identity continuityを保持し続けることができる。

withdrawn entryを、別のresearch objectのために黙って再利用してはならない。

revision historyはresearch provenanceの一部である。

---

## 10. Pastfold citationとunderlying historical source

Pastfoldは、以下として引用できる。

- research guide
- structured historical synthesis
- methodological interpretation
- editorial knowledge source
- machine-readable research resource

ただし、Pastfoldを引用することは、claimの根拠となっているunderlying historical sourceを引用することと常に同義ではない。

特定のprimary source、scholarly edition、archival record、inscription、chronicle、dataset、secondary workがclaimのevidentiary basisである場合、適切であれば、そのunderlying sourceを直接引用する。

Pastfold citationは、materialを整理・解釈・提示したresearch layerを特定する。

underlying-source citationは、claimが依拠するevidenceまたはscholarshipを特定する。

この2つの役割を混同しない。

---

## 11. precisionとmultiple-entry citation

claimが特定のperson、event、source、timeline、その他のentryに依存する場合、可能な範囲で最も具体的なrelevant entryを引用する。

よりspecificなentryが存在する場合、broad hubだけをprecise claimの唯一のcitationとして使うことは通常避ける。

argumentが複数のPastfold entryに依存する場合、それぞれのrelevant entryを個別に引用し、一つのgeneral citationへまとめすぎない。

これにより、individual claimとsupporting research objectの対応関係を保持できる。

---

## 12. machine-readable reuse

Pastfold-derived materialをAI system、retrieval index、dataset、embedding store、knowledge graph、その他machine-readable environmentへ保存または公開する場合、技術的・実務的に可能な範囲で以下を保持する。

- source name
- `entry_key`
- title
- language
- revision
- updated
- status
- canonical Markdown URL
- access date
- transformation type

追加で推奨されるmetadata:

- `entity_type`
- `content_type`
- `claim_status`
- period
- source limitation
- hypothesis-marker presence
- related `entry_key`
- license information

machine-readable reuseではprovenanceを保持し、transformed wordingやgenerated wordingをcanonical Pastfold textであるかのように扱ってはならない。

---

## 13. Article Specificationとの関係

Article Specificationは、Pastfold pageがどのmetadataを持つか、またどの責務がarticle bodyに属するかを定義する。

このポリシーは、pageが変更・引用・変換されたときに、その情報をどのようにtraceableな状態で保持するかを定義する。

具体的には:

- Article Specificationは `entry_key`、`revision`、`updated`、`status` を定義する
- Revision and Citation Policyは、それらのfieldがcontinuityとcitationをどう支えるかを定義する
- Article Specificationはmetadataとhistorical analysisの境界を定義する
- Revision and Citation Policyは、その境界をreuseとtransformationの過程でどう保持するかを定義する

この2つの文書は相補的である。

---

## 14. methodologyとの関係

このポリシーは、以下の文書とあわせて読む。

- Registry v2 Specification — durable identityとmanifestation mapping
- SANA Historical Reading Protocol — historical readingとanalytical practice
- Source Trifurcation — Fact、Perception、Record
- Three-Layer Analysis — Survival、Narrative、Institution

これらの文書は、それぞれ異なるlayerを担当する。

Registry v2はidentityとmanifestation mappingを保持する。

Article Specificationはpage structureを定義する。

Revision and Citation Policyはcontinuityとprovenanceを保持する。

methodology documentは、historical materialをどのように観察し解釈するかを定義する。

これらの責務を分離することで、content、language、URL、publication system、editorial structureが変化しても、Pastfoldはtraceableな状態を保ちやすくなる。
