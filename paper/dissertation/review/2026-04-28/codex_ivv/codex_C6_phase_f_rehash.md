# Codex C6: Phase F 외부 Mini-Rehash

작성: 2026-04-28 (codex IV&V Step 6)
대상: Phase F 적용 보고 (`applied_phase_f.md`) 8건 P0+P1 패치 + Q1 defense note
시각: cycle 1~3 + Phase F까지 모두 의도적으로 거리 두고 본문 verbatim만 재독한 외부 위원
상위 baseline: C0 종합 — 외부 보정 7.45 / strict 조건부 / defense 84–88%

---

## A. 8건 verbatim 검증 (C1 스타일)

| ID | 위치 | 본문 적용 | 평가 |
|----|------|----------|------|
| **M1** 라이선스 | `ch3:1015–1027` (subsec:code_data_availability) + `ch6:103` | **PASS** — "MIT License (MutBench's own implementation code)"·"CC-BY-NC 4.0"·`para:external_licenses`에서 ESM-2 MIT / ESM-3 Cambrian non-commercial *not used in headline* / Tranception MIT / EVE academic-only 모두 식별됨 | 약점: TODO 주석 2건 남아있음 (라이선스 정확 버전·KNU IBC 태그) — submission 직전 confirm 필요. ESM-3가 헤드라인 *not used*임을 명시한 것은 외부 위원 안심 포인트. |
| **M2** GenBank query | `ch3:133` | **PASS** — full SARS-CoV-2 query string (txid2697049, spike[Gene Name], 3500–4000nt, 2024-12-09) 본문 inline + 11 pathogen 전체는 `genbank_queries.csv`로 cross-reference | 약점: SARS-CoV-2 1건만 본문 inline. 다만 11건 모두 inline은 over-engineering이라 1건 + provenance CSV는 합리적 정공법. |
| **M3** worst-MCC | `ch4:340–342` (`para:stage2_worst_mcc`) | **PASS** — HCV×stability×SWAN(50,1.0)=−0.361, 4,171/8,580 (48.6%) MCC<0, plddt_inv/grantham/Tranception worst-mean 식별 | 강함: "pathogen-adaptive 헤드라인은 *bad cell의 부재*가 아니라 *ceiling vs floor의 큰 gap*에 anchor"라는 honest framing은 selective-reporting 비판을 사전 차단. |
| **D1** Vic/Yam | `ch3:71` 헤더 + `ch5:320–321` (`para:sublineage_pooling`) | **PASS** — CY018765가 Yamagata reference이지만 MSA는 Vic/Yam 혼합이고 lineage stratification 미수행임을 ch3에 honest, ch5에서 4 pooling case (Vic/Yam, pre-Omicron/Omicron, HIV-1 group/subtype, HCV genotype) 묶어서 acknowledge | D2/D3/D4 (Minor)는 *부분 처리* — 같은 §sublineage_pooling 단락에 묶어서 인정만 하고 re-run은 미수행. honest disclosure로는 충분. |
| **E1** DURC | `ch5:348–354` (`sec:durc_ethics`) | **PASS** — NIH/HHS DURC 7-카테고리 분류 + 모두 strict-policy 의미에서 해당 없음 (retrospective bioinformatic) + 3 mitigation + KDCA wet-lab 외부, KNU IBC 관할 명시 | 약점: KNU IBC review tag/letter ID는 `% TODO`. submission 시 confirm 필요. P3CO/Select Agent 한국 등치체계 명시는 굳이 추가 안 됨 — minor gap. |
| **G1** RNA-virus | `abstract:2` ("currently scoped to the RNA-virus single-position regime; 11 RNA viruses, surface glycoproteins, point substitutions only") + `ch1:48` + `ch6:84` | **PASS** — abstract 첫 문장에 한정 절 박혀 있음, ch6:84에서 DNA viruses/eukaryotic/prokaryotic 모두 explicit out of scope 명시. | 강함: "MutBench라는 이름이 향후 확장 인상을 준다"는 C4 우려를 abstract 첫 줄 한정자가 직접 차단. |
| **C1** CD-HIT/MMseqs2 | `references.bib` 2건 BibTeX + `ch3:133` 본문 인용 + `ch3:1023` 라이선스 단락 | **PASS** — `fu2012cdhit`, `steinegger2017mmseqs2` 신규 BibTeX 정합 (`grep` 결과 정상), 본문에서 "self-implemented Python hashing pass... functionally equivalent to running CD-HIT~\cite{fu2012cdhit} or MMseqs2~\cite{steinegger2017mmseqs2}" 문구로 인용 + clustering at <100%는 *적용하지 않았다*는 정직한 disclosure. | 강함: dedup tool 인용 누락이라는 reproducibility 정공법을 단 1단락으로 닫음. |
| **Q1** answer note | `defense_q1_answer_note.md` | **PASS as document** | 별도 평가 — §D 참조 |

**8/8 verbatim PASS**. Phase F 보고서가 cycle 1~3과 마찬가지로 under-claim 방향 (즉 보고에 적힌 것보다 실제로 본문에 더 들어가 있는 경우는 없었지만, 빠뜨린 보고도 없음).

`verify_dissertation.py` 90/0/0 PASS + xelatex 245p 0 errors 0 undefined citations는 신뢰도 높음 (객관적 빌드 산출물).

---

## B. 외부 시각 점수 재추정

### B.1 항목별 회복 (C3 vs Phase F 후)

| 항목 | C3 외부 보정 | **Phase F 후 외부 추정** | 회복 폭 | 근거 |
|------|------------|-----------------------|--------|------|
| **I (한계 honesty)** | 8.5 | **8.7** | +0.2 | DURC 명목 추가, Vic/Yam pooling 명시, RNA-virus 한정 강화는 honesty의 *완성도*를 한 단계 올림. 8.5→9.0의 격차 중 약 0.4 회복. |
| **C (방법론)** | 7.3 | **7.5** | +0.2 | CD-HIT/MMseqs2 인용·GenBank query 본문 inline·worst-MCC 공개는 *방법론 reproducibility*의 직접적 보강. 7.5는 strict thresh 7.0을 0.5 여유 확보. |
| **G (실용)** | 6.8 | **6.95** | +0.15 | RNA-virus 한정 강화는 *실용 주장의 reach*를 정직히 좁혔으나, prospective evidence 부재라는 본질적 약점은 미해결 (Phase F는 한정 강화일 뿐 prospective 측정이 아님). 7.0 thresh 경계 여전. |
| **H (서술)** | 8.1 | **8.15** | +0.05 | 라이선스·DURC·Vic/Yam paragraph 추가는 서술 *분량* 증가일 뿐 등급 격상은 아님. |
| 나머지 (A,B,D,E,F) | 그대로 | 그대로 | 0 | Phase F 패치 영향 없음. |

### B.2 종합

| 지표 | C3 외부 보정 | **Phase F 후 외부 추정** |
|------|------------|----------------------|
| Phase 4 평균 | **7.45** | **7.55** (+0.10) |
| Strict 합격 | 조건부 (G=6.8이 thresh 0.2 미달) | **조건부 PASS** (G=6.95로 여전히 thresh 0.05 미달, 그러나 거리 좁힘) |
| Lenient 80점 | 74.5 (B+) | 75.5 (B+ 상단) |
| Defense % | **84–88%** | **86–90%** (+2pp) |
| Unconditional pass | 50–60% | **58–65%** |

**해석**: Phase F는 *외부 시각 점수를 +0.10 회복*시켰고, *defense %를 2pp 회복*시켰다. C0의 "8건 처리 시 88% → 92% 복원"은 **과대** 추정 — 실제 외부 시각으로는 8건이 +2~4pp만 만들고, prospective evidence 부재가 G 항목 thresh 경계를 풀지 못한다. **C0의 "92% 복원"은 in-house 낙관 추정이고, 외부 정직 추정은 86–90%**.

---

## C. 잔여 P2/P3 12건 defense 차단 위험 평가

| ID | 카테고리 | 위험 등급 | defense 차단? | 근거 |
|----|---------|---------|--------------|------|
| **S1 Mantel** | 통계 | **Medium** | 아니오 (단발 질문 trigger 가능) | n=11 distance matrix 5분 cost. phylogenetic statistician이 위원에 있을 경우 "왜 안 했는가" 단발 질문 1회 가능 — 답: "Friedman + LOPO + 11-cluster bootstrap이 phylogenetic non-independence를 이미 부분 통제하며 Mantel은 후속 연구로 queued". 차단 trigger는 아님. |
| **S2 F1/AUROC** | 통계 | **Low–Medium** | 아니오 | `stage3_full_results.csv`에 F1 컬럼 *존재 확인*이 applied_phase_f §11에 명시. ch4 표에 1 컬럼 추가는 1단계 cost인데 미수행. 위원이 "F1도 같이 보여달라"하면 supplementary table 약속으로 회피 가능 (Chicco & Jurman 인용은 본문에 이미 있음). |
| **S3 Jackknife** | 통계 | **Low** | 아니오 | n=11에서 ≤1분 cost. Minor. 위원이 묻지 않을 가능성 높음. |
| **D2/D3/D4** Sub-lineage | 도메인 | **Low** | 아니오 | Phase F가 §sublineage_pooling 단락에서 묶어서 acknowledge. Vic/Yam (D1)이 가장 위험했고 D1은 P0로 처리됨. D2/D3/D4 단발 trigger 위험 낮음. |
| **E2** DMS data agreement | 윤리 | **Low** | 아니오 | ch3:external_licenses에서 Bloom-lab=CC-BY 등으로 명시. "academic-research terms" 일괄 표현은 위원 한 명이 "정확한 약관 인용"을 요구하면 borderline. |
| **E3** 한국 IBC | 윤리 | **Low** | 아니오 | KNU IBC 명시는 했으나 review tag TODO. 한국 위원장이 "review letter 어디 있나" 물으면 "submission 시 confirm" 답변으로 mitigation. |
| **G2** Severity Medium→High | 범위 | **Low** | 아니오 | 표 1셀 변경 cost. ch6 abstract·ch1 한정 강화로 사실상 mitigation 됨. |
| **G3** UTR/pseudogene | 범위 | **Low** | 아니오 | RNA-virus surface glycoprotein scope 명시로 implicit out-of-scope. |
| **C2** Foldseek/DALI | 인용 | **Low** | 아니오 | structural biologist 위원이 있을 경우 단발 질문 가능. |
| **C3** AlphaFold-Multimer | 인용 | **Medium** | 아니오 (그러나 SASA 해석 한정) | monomer SASA가 trimer interface에서 over-estimate된다는 점은 ch5에 1줄 acknowledge 권장이었으나 미수행. ch4 SASA AUC 결과 해석 한정. 구조생물학 위원의 단발 질문 trigger 가능. |
| **C4** HMMER | 인용 | **Low** | 아니오 | Minor. |

**종합**: 잔여 12건 중 **defense 차단 trigger는 0건**. Medium 등급 3건 (S1, S2, C3)이 단발 질문으로 학생 답변을 시험할 수 있으나, 모두 "supplementary로 queued / acknowledge in revision"으로 닫을 수 있는 답변 거리 안에 있음. **차단 위험은 P0+P1 8건이 봉쇄했다고 본다.**

---

## D. Q1 defense answer note 평가

### D.1 4-step 답변 품질

| Step | 시간 | 품질 |
|------|------|------|
| 1. Honest disclosure 인정 (15초) | "정답은 *맞습니다*. Prospective time-forward validation은... ch5:337 (\sec:prospective_validation_gap)에서 honest disclosure" | **좋음** — hostile 위원의 첫 instinct를 즉시 비활성화. ch5:337 anchor 직접 인용은 학생이 본문을 외워서 들어왔다는 신호. |
| 2. H3N2 pilot framing (20초) | "frequency single-feature... method-of-failure analysis... 4-feature core나 EqualWeight integration의 prospective 결과는 측정하지 않았습니다" | **좋음** — Q1의 함정 ("multi-source가 prospective도 frequency를 이긴다는 증거 어디?")을 정확히 분리. 학생이 *측정하지 않은 것*과 *측정한 것*을 구분하는 어휘를 가지고 있음을 보임. |
| 3. Contribution 경계 (20초) | "retrospective benchmark 인프라 / retrospective pathogen-dependent finding / retrospective external anchor에 한정" | **좋음** — *"그럼 학생이 지금 해결한 문제는?"* 이라는 Q1 후속 압박을 사전 차단. 3개 contribution 모두 *retrospective* prefix를 박은 것은 학생 자신감의 신호. |
| 4. Future work (10초) | "Priority 1로 등록... MutBench 인프라가 이를 받아들일 수 있는 상태로 설계" | **중간–좋음** — "받아들일 수 있는 상태"는 *후속 prospective 평가가 본 인프라 위에서 즉시 가능*함을 시사 → 학생의 contribution이 *prospective evaluation을 *enable*한다*는 메시지. 약점: "received state"라는 표현은 inteacher style보다 academic style이 적절. |

**총평**: 4-step 합계 65–80초, **hostile 위원에게 통한다**. ch5:337 verbatim ("A central honesty disclosure is that no \emph{prospective}, time-forward validation has been conducted...")이 학생 입에서 그대로 나오는 순간 위원이 부정직 의심을 가져갈 거리가 닫힌다. C0의 84–88% 추정에서 **Q1 fail trigger 거리는 본 노트가 충분히 닫는다**.

### D.2 후속 Q 대비 평가

- **Q1a "Why call it MutBench?"**: 답변에 "ProteinGym, ViroGym, EVEREST와 동일 framing"이라는 *외부 동급 brand* 인용이 들어있음. **좋음** — *brand 명칭이 retrospective benchmark의 학계 표준*임을 외부 anchor로 입증.
- **Q1b "3a/3b도 retrospective뿐?"**: 답변이 "예"로 단호히 시작하고 *non-rejection of inferiority*·*Bonferroni p_adj* 두 statistical 정확 표현으로 마무리. **좋음**.
- **Q1c "지금 학생이 해결한 문제는?"**: 답변 50단어로 (1) benchmark 인프라 부재 (2) 통계적 답변 부재 (3) 외부 검증 부재 — 세 *부재*를 *지금 해결*과 *지금 enable한 것*으로 끊어서 정의. **좋음** — 학생이 *지금 푼 것*과 *지금 풀 수 있게 만든 것*을 구별하는 메타 인식이 있음.

### D.3 위험 잔존

- 노트 §"피해야 할 표현" 3건 (특히 *"prospective도 사실상 됐다"*)을 학생이 stress 하에서 흘리지 않도록 **반드시 외워서 가야** fail trigger 거리에서 멀어진다.
- 슬라이드 마지막 limitation 1줄 ("3 honest disclosures: prospective gap, single anchor, Tranception–ESM proxy")은 노트의 압권 — Phase 0 사전 차단 효과가 가장 큰 단일 조치.

**Q1 defense note 품질**: **좋음 (defense에서 즉시 사용 가능)**. C5의 "fail trigger 근처"는 본 노트로 *fail trigger 1단계 멀어짐*.

---

## E. Phase F 새 결함 (있다면)

Phase F 패치 부작용/신규 결함을 외부 시각으로 검토:

1. **TODO 주석 2건**: `% TODO: confirm exact license version` (ch3:1016) + `% TODO: confirm KNU IBC review tag/letter ID` (ch5:354). xelatex 빌드는 통과하지만 **submission 직전 confirm 의무**가 본문에 박혀 있음. defense 시 위원이 PDF에 *TODO* 주석 자체는 보지 않으나, 발표 후 thesis archive 단계에서 cleanup 필수.

2. **Vic/Yam acknowledge-only**: ch5:320–321 §sublineage_pooling은 4 pooling case를 묶어서 acknowledge하지만 *re-run은 0회*. honest disclosure로는 충분하나, 위원이 "그럼 Vic/Yam 분리 후 best=freq 재계산해보면 어떻게 되는가"를 단발로 물으면 답변 거리 borderline (*sensitivity로 queued* 답변).

3. **ESM-3 Cambrian non-commercial 명시**: ch3:1025에서 "ESM-3 was *not* used in the headline 8,580-evaluation grid"라고 적은 것은 강한 honest disclosure이나, 본문에 ESM-3가 등장하는 다른 위치 (예: ch2 background, ch5 future work)에서도 같은 한정이 일관되게 적용되었는지 cross-chapter 일관성은 본 review 범위 밖. 잠재 risk: ESM-3 인용 위치 1곳이라도 *headline에서 사용되지 않음* qualifier 없이 등장하면 라이선스 honesty가 약해짐. *권고: ch2/ch5에서 ESM-3 등장 위치 1회 grep 후 일관성 점검*.

4. **CD-HIT 인용을 "functionally equivalent"로 처리**: ch3:133 본문이 *self-implemented Python hashing*과 *CD-HIT/MMseqs2의 100% identity threshold*가 functionally equivalent라고 적었으나, *왜 직접 tool을 쓰지 않았는가*에 대한 정당화는 없음. 위원이 "표준 tool 안 쓰고 직접 구현한 이유"를 묻으면 "100% identity exact-duplicate에서 둘은 산술적으로 identical하므로 추가 dependency를 도입할 가치가 없었다"는 답변이 가능하나 본문에 명시 안 됨. **Minor 잔존**.

5. **defense_q1_answer_note의 verbatim anchor 4건**: ch5:337, ch5:342, abstract:2, ch4:201. 본 review에서 ch5:337/abstract:2 모두 verbatim 일치 확인했으나 **ch4:201의 "frequency alone is retrospectively diagnostic but prospectively weak"** 문구는 본 review 범위에서 직접 grep으로 확인하지 않음 (Phase F 8건 scope 밖). 학생은 발표 전 ch4:201 verbatim을 다시 한 번 본문과 sync해야 함.

**총평**: Phase F는 새 결함을 **0건의 critical, 0건의 major, 5건의 minor (모두 cleanup-level)**로 introduce했다. 부작용 리스크는 cycle 1~3 패치 round 평균 대비 낮음.

---

## F. 종합 외부 판정

| 지표 | C0 baseline | **Phase F 후 외부 추정** | 변동 |
|------|------------|----------------------|------|
| Phase 4 평균 | 7.45 | **7.55** | +0.10 |
| Strict 합격 | 조건부 (G=6.8) | **조건부** (G=6.95, thresh 0.05 미달) | 약간 회복 |
| Lenient | 74.5 (B+) | 75.5 (B+ 상단) | +1.0 |
| Defense % (학위 통과) | 84–88% | **86–90%** | +2pp |
| Unconditional pass | 50–60% | **58–65%** | +8pp |
| 잔여 결함 | 20건 | **12건 (모두 minor/no-defense-trigger)** | -8 |
| Q1 fail trigger 거리 | 가까움 | **1단계 멀어짐** | 회복 |

### 핵심 결론

1. **Phase F 8건 모두 본문에 verbatim 적용** (8/8 PASS). 보고서는 cycle 1~3과 동일하게 under-claim 방향.
2. **외부 시각 점수 7.45 → 7.55 (+0.10 회복)**. C0가 추정한 "92% 복원"은 **과대**, 정직 추정은 86–90%.
3. **잔여 12건은 defense 차단 trigger 0건**. Medium 3건 (S1 Mantel, S2 F1/AUROC, C3 AlphaFold-Multimer)은 단발 질문 trigger 가능하나 모두 *supplementary로 queued* 답변 거리 안.
4. **Q1 defense note 품질 좋음**. ch5:337 verbatim + 4-step 65–80초 + 후속 Q1a/b/c 답변 모두 hostile 위원에게 통한다. fail trigger 거리 1단계 멀어짐.
5. **Phase F 신규 결함 0 critical / 0 major / 5 minor (cleanup-level)**. 부작용 낮음.

### 권고 (외부 시각, 우선순위 순)

| 우선 | 액션 | 시간 | 영향 |
|-----|------|-----|-----|
| **P0** | TODO 주석 2건 confirm (라이선스 버전 / KNU IBC 태그) — submission 직전 | 1시간 | 라이선스/윤리 honesty 완성 |
| **P0** | 학생이 Q1 답변 노트 verbatim 외워서 들어가기 + 슬라이드 마지막 *3 honest disclosures* 1줄 | 학생 자체 작업 | fail trigger 거리 추가 1단계 |
| **P1** | S2 F1/AUROC supplementary table (`stage3_full_results.csv` 기반 1 컬럼 추가) | 30분 | unconditional pass 확률 +5pp |
| **P1** | C3 AlphaFold-Multimer 1줄 acknowledge (ch5 SASA 해석 한정) | 5분 | 구조생물학 위원 단발 질문 봉쇄 |
| **P2** | ESM-3 cross-chapter 일관성 grep (ch2/ch5에서 *not used in headline* qualifier 부재 위치 점검) | 10분 | 라이선스 honesty cross-chapter 일관성 |
| **P3** | 나머지 9건 (S1/S3/D2/D3/D4/E2/E3/G2/G3/C2/C4) — defense 후 patch 가능 | --- | --- |

### 외부 판정

**조건부 PASS (학위 통과 86–90%)**.

unconditional pass는 G 항목이 thresh 0.05 미달이라 여전히 어렵다 (58–65%). 그러나 **prospective evidence 부재 외에는 더 이상 fail trigger가 본문에 남아있지 않으며, prospective 부재는 Q1 defense note로 trigger 거리에서 멀어졌다**. C0가 식별한 8 blind spot 차원 중 *licensing / GenBank query / negative-result reporting / sub-lineage stratification (intentional pooling) / DURC formal compliance / structural-tool citation breadth (CD-HIT/MMseqs2)* 6개는 닫혔고, *Mantel/Procrustes alternate distance-matrix tests / AlphaFold-Multimer (구조 tool breadth 일부)* 2개는 acknowledge-only로 부분 닫힘.

Phase F는 cycle 1~3 framework 밖의 8 차원 blind spot 중 **다수 closed, 일부 acknowledge-only**로 처리한 정공법 round였다. 외부 시각으로 honest 회복 폭은 +2pp이고, **현 상태에서 defense 진입 권고 가능**.
