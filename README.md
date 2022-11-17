
# Japanese Realistic Textual Entailment Corpus

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>
[![CI](https://github.com/megagonlabs/jrte-corpus/actions/workflows/ci.yml/badge.svg)](https://github.com/megagonlabs/jrte-corpus/actions/workflows/ci.yml)
[![Typos](https://github.com/megagonlabs/jrte-corpus/actions/workflows/typos.yml/badge.svg)](https://github.com/megagonlabs/jrte-corpus/actions/workflows/typos.yml)

## Overview

This corpus contains examples labeled whether the premise entails the hypothesis or not as follows.

```txt
Hypothesis: 部屋から海が見える。 (You can see the ocean from your room.)
Premise   : 部屋はオーシャンビューで景色がよかったです。 (The room had an ocean view and a nice view.)
Label     : Entailment
```

All examples utilize texts in Japanese hotel reviews posted on [Jalan](https://www.jalan.net/), which is a travel information web site.
This corpus also contains sentences with sentiment polarity labels and labels whether the text is hotel reputation or not as follows.

```txt
Text            : 朝食が美味しいです。 (The breakfast is delicious.)
Sentiment       : Positive
Hotel reputation: True
```

⚠ **Because some of the data have been removed for various reasons, this corpus does not exactly correspond to one used in the reference papers.**

## Description

All files are in the Tab-separated values (TSV) format.
All texts are Unicode NFKC normalized.

### data/rte.*.tsv

Data for textual entailment.

| # | Explanation | Samples |
| ---   | --- | ---    |
| 0     | ID of the example | ``rteXYZq00001`` |
| 1     | Label | ``1`` (Entailment), ``0`` (Non-entailment) |
| 2     | Hypothesis | ``駅まで近い。``      |
| 3     | Premise   | ``温泉は、肌がスベスベになります。`` |
| 4     | Judges (JSON format)  |  ``[{"0": 5, "1": 0}, {"0": 0, "1": 2}]``|
| 5     | Reasoning (JSON format) | ``[["駅まで", 3], ["近い", 0], ["<unknown>", 1], ["<1>", 1]]`` |
| 6     | Usage | ``train``, ``dev``, ``test`` |

#### Description of "Judges"

This is a collection of binary judgments of the annotators, represented by a ``dictionary``.
The key is the choice and the value is the number of people who chose the choice.
When the binary annotation is not performed, this is ``null``.
If you ask more than once, this is a ``list`` of ``dictionary``.
Basically, the label is majority voted, but some are corrected manually.

#### Description of "Reasoning"

This is the result of the annotator's selection from tokens in ``Hypothesis`` for Non-entailment examples, represented by a ``list``.
When the annotation is not performed, this is ``null``.
There are two special tokens: ``<1>`` (The label is entailment) and
``<unknown>`` (Difficult to specify tokens)

#### Description of "Usage"

The usage of the example for papers.
In reference papers, we used example labeled as ``dev`` for training because we have not tuned hyperparameters.

#### Files

- ``rte.nlp2020*.tsv``: Data used in ["NLP 2020"](#references)
    - ``rte.nlp2020_base.tsv``: ``BASE``
    - ``rte.nlp2020_append.tsv``: ``APPEND``
- ``rte.lrec2020*.tsv``: Data used in ["LREC 2020"](#references)
    - ``rte.lrec2020_surf.tsv``: ``Surf`` in ``BASE``
    - ``rte.lrec2020_sem_short.tsv``: ``SemShort`` in ``BASE``
    - ``rte.lrec2020_sem_long.tsv``: ``SemLong`` in ``BASE``
    - ``rte.lrec2020_me.tsv``: ``ME``
    - ``rte.lrec2020_mlm.tsv``: ``MLM``

#### data/operation.rte.lrec2020_mlm.tsv

An explanation of how we generated the ``MLM`` data.

| # | Explanation | Samples |
| ---   | --- | ---    |
| 0     | ID of the example | ``rteXYZq00001`` |
| 1     | ID of the original example | ``rteABCq00001``|
| 2     | Operation | ``insert``, ``replace`` |
| 3     | Target | ``hypothesis``, ``premise`` |

### data/rhr.tsv

Data for recognition of hotel reputation.

| # | Explanation | Samples |
| ---   | --- | ---    |
| 0     | ID of the example | ``rhrXYZq00001`` |
| 1     | Label | ``1`` (Hotel reputation), ``0`` (Not hotel reputation) |
| 2     | Text | ``お風呂が最高でした。``, ``1人旅で利用しました。`` |
| 3     | Judges (JSON format)  |  ``{"0": 1, "1": 2}``|
| 4     | Usage | ``train``, ``dev``, ``test`` |

### data/pn.tsv

Data for sentiment analysis.

| # | Explanation | Samples |
| ---   | --- | ---    |
| 0     | ID of the example | ``pnXYZq00001`` |
| 1     | Label | ``1`` (Positive), ``0`` (Neutral), ``-1`` (Negative) |
| 2     | Text | ``駅まで近い。``      |
| 3     | Judges (JSON format)  |  ``{"0": 1, "1": 4}``|
| 4     | Usage | ``train``, ``dev``, ``test`` |

## References

1. 林部祐太．
    知識の整理のための根拠付き自然文間含意関係コーパスの構築．
    言語処理学会第26回年次大会論文集，pp.820-823. 2020. (NLP 2020)
    [[PDF]](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P4-9.pdf)
    [[Poster]](https://storage.googleapis.com/megagon-publications/nlp2020/p4-9_hayashibe_poster.pdf)
2. Yuta Hayashibe.
    Japanese Realistic Textual Entailment Corpus.
    Proceedings of The 12th Language Resources and Evaluation Conference, pp.6829-6836. 2020. (LREC 2020)
    [[PDF]](https://www.aclweb.org/anthology/2020.lrec-1.843.pdf)
    [[bib]](https://www.aclweb.org/anthology/2020.lrec-1.843.bib)

## Notes

- 株式会社リクルート（以下「リクルート」といいます。）は自然言語処理の研究に貢献する目的で、言語的注釈が付与されたデータセット（以下「本データセット」といいます。）を公開いたします。
- Recruit Co., Ltd.(hereinafter referred to as "Recruit") publishes the data set with linguistic annotations (hereinafter referred to as this "Data Set") for the purpose of contributing to the study of natural language processing.

- 本データセットには、クチコミデータから抽出した文、それらを加工した文、アノテーション作業者が付与した判定ラベルが含まれます。ラベルは作業者によって付与されたものであり、クチコミ投稿者の体験や評価、もしくはリクルートの評価を反映したものではありません。
- This Data Set is constructed using various methods of extraction from Customer Reviews. Annotators provide judgment via labels. Labels and recommendation sentences are provided by the cloud-sourced annotators and do not reflect the experience, assessment, or Recruit’s assessment of the review contributor.

- 事実と異なる内容が含まれる場合があります。
- This Data Set may contain content that is contrary to the facts.

- 本データセットは通知なく変更・削除される場合があります。
- This Data Set is subject to change or deletion without notice.

## License and Attribution

- 本データセットに含まれる「じゃらんクチコミデータ」の著作権は、リクルートに帰属します。
- The copyrights to Customer Reviews included in this Data Set belong to Recruit.

- 本データセットを用いた研究発表を行う際は、[References](#references)の論文を引用し、次のようにデータの入手元も記述してください。
    - 文例： 本研究では株式会社リクルートが提供する"Japanese Realistic Textual Entailment Corpus" (``https://github.com/megagonlabs/jrte-corpus``)を利用しました。
- When publishing a study using this dataset, please cite papers in [References](#references) and describe the source of the data as follows.
    - Example: To conduct this study, we used "Japanese Realistic Textual Entailment Corpus" (``https://github.com/megagonlabs/jrte-corpus``) provided by Recruit Co., Ltd.

- 本データセットのライセンスは[クリエイティブ・コモンズ・ライセンス (表示-非営利-継承 4.0 国際)](https://creativecommons.org/licenses/by-nc-sa/4.0/)です。
- The license of this Data Set is in the same scope as [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Prohibitions

- リクルートは本データセットを非営利的な公共利用のために公開しています。分析・研究・その成果を発表するために必要な範囲を超えて利用すること（営利目的利用）は固く禁じます。
- Recruit discloses this Data Set for non-profit public use. It is strictly prohibited to use for profit purposes beyond the scope necessary for the presentation of analysis, research and results.

- 利用者は、研究成果の公表といえども、前項の出版物等の資料に、適正な例示の範囲を超えてデータセット中のデータを掲載してはならず、犯罪その他の違法行為を積極的に助長・推奨する内容や公序良俗に違反する情報等を記述しないでください。
- Even when publishing research results, users should not post data in the data set beyond the appropriate exemplary range in the publications and other materials set forth in the preceding paragraph. Users should not describe information obtained from the data set that violates public order and morals, promote or encourage criminal or other illegal acts.

## Contact

If you have any inquiries and/or problems about a dataset or notice a mistake, please contact NLP Data Support Team ``nlp_data_support at r.recruit.co.jp``.
