# Codex C4: 외부 적대적 새 공격 (cycle 1~3 Blind Spots)

검수자: 외부 codex IV&V (cycle 1~3 결함 list 미열람 시각)
대상: ch1~ch6 + abstract.tex
목적: cycle 1~3이 같은 프레임워크를 공유하면서 못 본 차원의 결함 발견

---

## 1. 메타-결함 (cycle 1~3 차원 외)

### M1. 제3자 모델/score 라이선스 미명시 (Critical)
**file:line**: ch3:1013, ch3:677, ch3:716, ch6:101
- ch3:1013은 *MutBench 본인 코드*만 "released under an open-source license"라고 적었지만, **어떤 라이선스인지 명시 안 됨** (MIT? Apache 2.0? GPL? CC-BY?). GitHub repo 링크만 있다.
- 더 중요한 점: 본문은 ESM-2 (Meta — non-commercial), Tranception (Notin et al. — research-only), EVEscape (Thadani — methods), AlphaFold-DB (DeepMind — CC-BY 4.0), HyPhy (GPL) 등 라이선스가 서로 충돌할 수 있는 외부 모델/score를 \emph{재배포 형식이 아닌 score 산출물 형태로} 사용하는데, 그 산출물을 GitHub + Zenodo로 공개할 때의 \textbf{라이선스 호환성 검토 흔적이 본문 어디에도 없다.}
- ESM-2 weights 라이선스(Meta non-commercial)와 mutbench의 "open-source" 라이선스가 호환되는지가 명시되지 않음. 외부 reviewer가 "이 score는 non-commercial 모델 결과인데 너의 open-source 배포가 그 약관을 위반하는지 어떻게 보장하는가"를 물으면 답변 불가.
- 위험도: **Critical** (defense에서 reviewer 1명만 라이선스 전문가여도 직격).

### M2. GenBank query 재현성 — 본문에 query 문자열이 없다 (Major)
**file:line**: ch3:131-164
- 본문은 `query date`만 표에 적고, 실제 GenBank advanced-search 표현식은 `results/mutbench/provenance/genbank_queries.csv`에 외부 archive로 deferred. 즉, **dissertation 내부 만으로는 11 pathogen 중 어느 하나도 재현 불가능**.
- cycle 1~3은 "query date 적었으니 OK"로 통과시켰지만, query date만으로는 같은 GenBank set을 못 만든다 (taxonomy ID, length filter, exclude clause 등 불특정). 표에 올라간 11개 \emph{N} 값(예: SARS-CoV-2 4,982; H3N2 2,644)이 reviewer가 동일 query date에 같은 query를 돌렸을 때 ±10% 이내로 재현되는지 입증 불가.
- 위험도: **Major** (defense reproducibility Q에서 Zenodo가 아직 placeholder DOI라 즉답 불가).

### M3. 8,580 evaluation 중 worst-perform 조합의 비공개 (Major)
**file:line**: ch4:303 (Table 2 stage2_best는 best만), ch4:425, abstract:11
- 본문은 \emph{best} 조합만 표 + 본문에 보고. 8,580개 중 \textbf{최저 MCC} 조합 / 음의 MCC 조합 수가 한 번도 본문에 나오지 않음. ch4:483 selective-reporting probe가 "second-best gap"은 archive에 있다고 적었지만, "worst-detector" "worst-scoring" "negative-MCC count"는 archive에도 언급 없음.
- Best만 보여주는 것은 paper-plan 4-Phase의 "selective reporting" 판정 기준이고, cycle 1~3 어디서도 worst-end를 요구하지 않은 것은 \textbf{공유 blind spot}. 8,580 중 음의 MCC 비율은 통상 30~40% 인데, 이를 보고하지 않으면 "이 정도면 random보다 더 나쁜 조합도 많다"는 reviewer의 직관적 의구심을 미리 차단할 수 없다.
- 위험도: **Major**.

---

## 2. 통계 대안 검정

### S1. Mantel test / Procrustes 부재 — pathogen-pathogen 거리 일치 검정 안 함 (Major)
**file:line**: ch4:425-528 전체, ch5:289
- 본문은 ANOVA + Friedman + LOPO + permutation + cluster bootstrap + ANCOVA + Bayesian + ART를 다 돌렸다. 하지만 \textbf{병원체 간 거리 행렬} (예: scoring-rank 거리 vs phylogenetic 거리, 또는 scoring-rank 거리 vs evolutionary-rate 거리)의 일치를 검정하는 **Mantel test 부재**.
- "scoring × pathogen interaction이 phylogenetic relatedness와 무관"이라는 ch5:327 주장은 **표면적 family-pair 비교** ("H3N2 vs B는 best 다르다")만으로 입증되었고, Mantel correlation r·p 같은 정량 검정은 없음. Mantel은 phylogenetic non-independence 평가의 표준 도구라 이 검정 부재는 통계 종합성의 큰 구멍.
- 위험도: **Major** (defense에서 phylogenetic statistician이 1명만 와도 "왜 Mantel 안 했나" 질문 가능).

### S2. Headline metric 선택 — F1 / AUROC 동시 보고 안 함 (Minor → Major 누적)
**file:line**: abstract:10, ch3:881-892, ch4:540 Table
- 본문이 stage 2 headline을 MCC \emph{단일}로 채택하면서, 같은 8,580 cell에서 동시에 계산 가능한 F1 / AUROC를 본문 어디에서도 \emph{병기}하지 않음. ch3:885은 F1을 "computed"한다고 적었으면서도 결과 표는 MCC만 등장.
- Chicco & Jurman 인용 (ch3:907)으로 MCC 선택을 정당화했지만, MCC가 정합 metric이라는 주장과 \emph{F1/AUROC를 같이 안 보여줘도 된다}는 주장은 다름. 공정성 reviewer는 "당신이 보여주고 싶은 metric만 골랐다"고 할 수 있다.
- 위험도: **Major**. \texttt{stage3\_full\_results.csv}는 F1·AUROC 컬럼을 포함할 가능성이 있는데 본문에서 한 번도 인용/표시 안 함.

### S3. Bootstrap 재표집 — Jackknife 미시도 (Minor)
**file:line**: ch3:953, ch4:525
- BCa bootstrap (1,000–10,000 resamples) + cluster bootstrap (1,000) + paired bootstrap (1,000) + sign-flip permutation (5,000)는 모두 보고. **delete-one jackknife** ($n=11$이라 정확히 11회면 충분, 매우 저렴)는 한 번도 시도 안 됨.
- $n=11$ small-cluster 영역에서 jackknife는 BCa bootstrap의 acceleration 항을 직접 제공하는 표준 도구. 11번이면 분석 1분 내 끝나는데 안 한 것은 "small-cluster 정공법 회피"로 비칠 수 있음.
- 위험도: **Minor** (그러나 cycle 1~3 wild-cluster bootstrap deferral과 함께 누적되면 Major 인상).

---

## 3. 도메인 적대

### D1. Influenza B Victoria/Yamagata 분리 결과 부재 (Major)
**file:line**: ch3:68-72, ch4:316, ch4:361
- 본문은 Influenza B를 \emph{단일 pathogen}으로 취급. 그러나 ch3:70에서 본인이 인정했듯 Victoria와 Yamagata 두 lineage가 1980년대부터 \textbf{co-circulation}하고, MSA에 둘이 섞여 있다. 이는 곧 Layer~A의 "best feature = freq" (ch4:318)가 lineage-defining 변이 (Vic vs Yam-specific 위치)를 잡고 있을 가능성이 매우 높음을 시사.
- ch5:319 "scope justification"에서 viral family 다양성은 따졌지만, **subtype 내부 lineage split**의 영향은 한 번도 ablation 안 됨. Mann-Whitney $U$나 lineage-specific 재계산 없음.
- 위험도: **Major**. defense에서 H3N2/Influenza B 전문가가 "두 lineage를 한 데 합쳐서 freq 찍은 것은 systematic bias 아니냐"고 물으면 즉답 불가.

### D2. HIV-1 group M / O 분리 미명시 (Minor)
**file:line**: ch3:77-83
- HIV-1을 단일 pathogen으로 취급. group M (대다수) vs group O (서아프리카, ≤1% 빈도) 분포 명시 없음. group M 내부 subtype A/B/C도 미분리. Haddox 2018 DMS는 group M subtype B인데 (BG505 base), Layer~A (Moore-Williamson 2015)도 group M subtype 위주.
- "HIV-1 entropy=best (MCC 0.275)" (ch4:319)이 group/subtype mixing 효과인지 진짜 entropy 신호인지 분리 불가.
- 위험도: **Minor**. HIV-1이 contribution 3b 핵심 anchor (Bonferroni $p_\text{adj}=2.5\times10^{-16}$)이므로 reviewer가 HIV-1 detail을 깊게 파면 우려 사항.

### D3. SARS-CoV-2 시점 분리 — Omicron 시점의 score 변화 분석 부재 (Major)
**file:line**: ch3:42 (data: 2019–2024), ch5:266-268 (temporal window)
- 본문은 SARS-CoV-2 sequence를 2019–2024 \emph{한 덩어리}로 평균 처리. ch5:267은 "frequency AUC가 2020-H1 0.337 → 2021-H1 0.472로 변한다"는 temporal-window analysis를 1줄 언급할 뿐, **Omicron (2022~) 시점의 score는 무엇이었는지** 본문에 없음. PANGO BA.2.86/JN.1 (ch2:178)을 인용했으면서도 그 시점 데이터로 ch4 결과 재계산은 누락.
- "SARS-CoV-2 best = Tranception" (ch4:323)이 \textbf{어느 시점} 기준인지 본문에 명시 없음. 2020만 보면 best가 freq, 2024만 보면 best가 다른 것일 수도 있음.
- 위험도: **Major**.

### D4. HCV genotype 1 vs 3 분리 부재 (Minor)
**file:line**: ch3:84-89
- HCV 7개 genotype이 있는데 본문은 NC_004102.1 (genotype 1a) reference만 쓰고 genotype별 분리 없이 평균 처리. HCV best=freq MCC 0.660 (ch4:315)이 genotype clustering 효과인지 진짜 신호인지 분리 불가.
- 위험도: **Minor**.

---

## 4. 공정성 / 윤리

### E1. DURC 검토 명시 부재 (Major)
**file:line**: ch6:98 (Dual-use considerations 단락)
- ch6:98이 dual-use 위험을 인정하고 3가지 mitigation을 제시한 것은 cycle 1~3 patch 결과로 보임. 그러나 \textbf{DURC (Dual Use Research of Concern)} 명목 자체를 본문이 안 부른다. 미국 NIH/HHS의 DURC framework는 7개 카테고리 (transmissibility 증가, immune-escape engineering 포함) 중 어디에 해당하는지 명시할 의무가 있는데, 그 분류 진술이 빠짐.
- "P3CO/Select Agent lists" 언급은 했지만 그것은 DURC와 별개 framework. 한국 IBC 검토를 거쳤는지도 표시 없음.
- 위험도: **Major**. 한국 IBC/IRB 의무 위반 가능 (실험은 없지만 computational dual-use는 2024 이후 IRB 검토 권고).

### E2. DMS 데이터 사용에 대한 IRB/permission 명시 부재 (Minor)
**file:line**: ch3:325 (DMS sources), ch2:109
- Layer~C에서 6개 pathogen DMS data를 사용 (Dadonaite 2024 SARS-CoV-2; Lee 2018 H3N2; Haddox 2018 HIV-1; Simonich 2026 RSV; Aditham 2025 Rabies; Bakhache 2025 EV-A71). 모두 publication에 attached한 처리된 fitness table이라 IRB 의무는 없을 가능성 높지만, **약관 (data use agreement) 확인 흔적이 본문 0건**.
- HIV-1 Haddox 2018은 Dryad에 deposit되어 CC0/CC-BY 가능성 높지만 본문에 명기 안 됨.
- 위험도: **Minor**.

### E3. 한국 KCDC / 국내 윤리 framework 적용 흔적 부재 (Minor)
**file:line**: ch6:98
- 한국 박사논문이라면 한국질병관리청 (KDCA) 또는 IBC 절차가 있을 수 있음. ch6:98은 미국 HHS P3CO만 언급. 국내 절차 인용 0건.
- 위험도: **Minor** (한국 위원장 교수가 지적할 가능성 있음).

---

## 5. 범위 / generalization

### G1. RNA virus 한정자 vs benchmark 명칭의 misalignment (Major)
**file:line**: abstract:2 ("MutBench, region-level"), ch1:33-39, ch6:96
- "MutBench"라는 이름은 일반 mutation benchmark를 시사하지만, 실제 scope는 RNA virus surface protein only. ch5:319-322가 이를 honest하게 적었지만, **abstract는 "MutBench" 단독 명사를 RNA-virus 한정 없이 쓴다** (abstract:2 "broadest region-level... benchmark to date for RNA viruses"는 후위 한정에 가깝다).
- title page는 본 task에서 보지 못했지만, abstract 첫 줄이 "11 RNA viruses"라고 박혀있어 어느 정도 mitigation은 있음. 그러나 "MutBench"라는 메타 brand가 향후 DNA virus / 박테리아로 확장될 인상을 안긴다 — defense reviewer가 "왜 이렇게 큰 이름을 쓰나"고 물으면 약점.
- 위험도: **Major**.

### G2. Eukaryotic / bacterial pathogen 검증 부재 — 명시는 있지만 일반화 한계 약하게 표시 (Minor)
**file:line**: ch6:39 (Limitations table), ch6:63 (Future work)
- ch6:39 "RNA viruses and surface proteins only" 한계 표가 있지만, severity가 **"Medium"**으로 기재됨. 그러나 11/11 pathogen이 모두 RNA virus + surface protein이므로 이는 \textbf{High severity scope limitation}으로 격상되어야 함.
- ch5:330 PLM-data limitation 단락도 단지 "training-data overlap" 차원만 짚었지 "non-RNA virus 검증 0건"은 0건이라고 적시 안 함.
- 위험도: **Minor**.

### G3. Non-protein-coding region (UTR) / non-coding selection 처리 명시 없음 (Minor)
**file:line**: ch3 전체, ch6:39
- 본문이 surface protein coding region만 쓰는 것은 표 ch3:138 reference accession의 의미상 명확하지만, "5'UTR / 3'UTR / IRES / non-coding selection"이 명시적으로 out-of-scope로 적힌 곳 없음. RSV의 경우 UTR-local selection이 documented.
- "pseudogene / readthrough" handling도 0번 언급. EV-A71 / Norovirus는 readthrough 없지만, HCV는 polyprotein cleavage가 있어 "single-protein scope" 한계가 사실상 polyprotein 일부만 평가하는 셈.
- 위험도: **Minor**.

---

## 6. 인용 누락 (cycle 1~3 미점검 분야)

### C1. MMseqs2 / CD-HIT — sequence dedup tool 인용 누락 (Major)
**file:line**: ch3:131
- ch3:131 "identical sequences were deduplicated" — \textbf{어떤 tool로} dedup 했는지 명시 없음. CD-HIT (Fu et al. 2012)? MMseqs2 (Steinegger \& Söding 2017)? 자체 Python script?
- 11 pathogen 중 8개의 unique seq ratio가 60-100%인데, dedup tool 선택은 reproducibility의 1단계. 특히 SARS-CoV-2 (753/4,982 = 15.1%)에서 어떤 identity threshold를 썼는지 미명시 — 100% identical만? 99% identity? 그 결과가 8,580 evaluation의 입력 데이터 자체를 결정.
- 위험도: **Major**.

### C2. Foldseek / DALI — 구조 유사도 도구 미인용 (Minor)
**file:line**: ch3:643-672 (structural feature, Table tab:structure_sources)
- pLDDT/SASA는 ESMFold per-pathogen으로 계산. 그러나 "structure quality 검증"을 위한 Foldseek (van Kempen 2024) 또는 DALI (Holm 1993) 같은 \textbf{predicted-vs-experimental 구조 alignment} tool이 한 번도 인용 안 됨.
- ch5:332 "structure quality varies"라고만 적었지, 실제 SARS-CoV-2 AlphaFold-DB가 cryo-EM PDB 6VSB (ch3:568)와 RMSD 얼마나 일치하는지 quantitative anchor 없음. AlphaFold2 vs ESMFold per-pathogen comparison도 없음.
- 위험도: **Minor**.

### C3. AlphaFold-Multimer — 한 번도 안 부름 (Minor)
**file:line**: ch3:643, ch4:254 (3D contact analysis on PDB 6VSB Spike trimer)
- SARS-CoV-2 Spike는 trimer로 작동하고 ch4:254가 "trimer cryo-EM structure"를 사용했다. 그러나 ESMFold는 \textbf{단량체 prediction}만 한다. 다른 10 pathogen의 예측 구조가 trimer/dimer assembly가 필요한데 (HIV-1 gp120 trimer, RSV F trimer, Influenza HA trimer, Dengue E dimer 등) AlphaFold-Multimer (Evans et al. 2022) 인용 없이 monomer ESMFold만 사용한 것은 surface accessibility (SASA) 계산의 \textbf{생물학적 정합성을 깬다}.
- monomer SASA는 trimer interface에서 \emph{과대 평가}된다 (실제 trimer assembly에서 가려지는 영역도 monomer에서는 노출). 이는 ch4 SASA AUC 결과의 직접적 해석 한계.
- 위험도: **Minor → Major** (구조생물학 reviewer 한정).

### C4. HMMER — homology-based filtering 인용 부재 (Minor)
**file:line**: ch3:131
- GenBank query에서 keyword filter만 사용. HMMER (Eddy 2011) 같은 HMM-based homology filter를 안 쓴 것은 frame-shifted 또는 partial-domain 시퀀스가 dataset에 들어왔을 가능성을 만든다. "complete coding sequences" filter가 GenBank flag만 의존하면 mis-annotation 가능성 잔존.
- 위험도: **Minor**.

---

## 발견 결함 표

| ID | 카테고리 | file:line | 결함 | 위험도 |
|----|---------|-----------|------|-------|
| M1 | 메타 | ch3:1013, ch3:677, ch3:716, ch6:101 | 라이선스 미명시 (MutBench 본인 + ESM-2/Tranception 호환성) | **Critical** |
| M2 | 메타 | ch3:131-164 | GenBank query 문자열 본문 부재 (CSV deferral만) | **Major** |
| M3 | 메타 | ch4:303, abstract:11 | 8,580 중 worst 조합 / 음의 MCC count 비공개 | **Major** |
| S1 | 통계 | ch4:425-528 | Mantel test / Procrustes 부재 (phylogenetic-distance vs scoring-distance 일치 검정) | **Major** |
| S2 | 통계 | abstract:10, ch3:881 | F1 / AUROC headline 병기 부재 (MCC 단독) | **Major** |
| S3 | 통계 | ch3:953 | Jackknife 미시도 ($n=11$에서 ≤1분 cost) | Minor |
| D1 | 도메인 | ch3:68, ch4:316 | Influenza B Victoria/Yamagata lineage 분리 없음 | **Major** |
| D2 | 도메인 | ch3:77 | HIV-1 group M/O / subtype 분리 없음 | Minor |
| D3 | 도메인 | ch3:42, ch5:266 | SARS-CoV-2 Omicron 시점 분리 결과 부재 | **Major** |
| D4 | 도메인 | ch3:84 | HCV genotype 1/3 분리 없음 | Minor |
| E1 | 윤리 | ch6:98 | DURC 명목 자체 미사용 (P3CO만 언급) | **Major** |
| E2 | 윤리 | ch3:325 | DMS data use agreement 명시 부재 | Minor |
| E3 | 윤리 | ch6:98 | 한국 KCDC/IBC framework 인용 부재 | Minor |
| G1 | 범위 | abstract:2, ch6:96 | "MutBench" 명사 vs RNA-virus 한정자 misalignment | **Major** |
| G2 | 범위 | ch6:39 | RNA-virus-only 한계 severity가 Medium → High 격상 필요 | Minor |
| G3 | 범위 | ch3 전체 | UTR / pseudogene / readthrough out-of-scope 명시 부재 | Minor |
| C1 | 인용 | ch3:131 | sequence dedup tool (CD-HIT/MMseqs2) 인용 부재 | **Major** |
| C2 | 인용 | ch3:643 | Foldseek/DALI 구조 유사도 검증 부재 | Minor |
| C3 | 인용 | ch3:643, ch4:254 | AlphaFold-Multimer 부재 → monomer SASA 한계 | Major |
| C4 | 인용 | ch3:131 | HMMER homology filter 부재 | Minor |

총 신규 결함 **20건** (Critical 1, Major 9, Minor 10).

---

## cycle 1~3 thoroughness 평가

| 차원 | cycle 1~3 점검 강도 | 평가 |
|------|------------------|------|
| 통계 robustness (ANOVA, bootstrap, ANCOVA, Bayesian, ART) | **High** (Phase 2 statistics 전용 phase) | cycle 1~3 충실 |
| Verbatim-claim consistency (한·영 sync, 14수치) | **High** (cycle 3 phase E 7건 patch) | cycle 1~3 충실 |
| Layer A/B/C circularity audit | **High** (Greaney mis-anchor / EqualWeight audit) | cycle 1~3 충실 |
| **저자 대 외부 모델 라이선스** | **None** | **신규 blind spot** |
| **GenBank query 본문 제시** | None (provenance CSV로 deferral) | **신규 blind spot** |
| **8,580 worst-end / negative MCC 보고** | None | **신규 blind spot** |
| **Mantel/Procrustes 등 거리행렬 검정** | None | **신규 blind spot** |
| **F1/AUROC 병기** | None (MCC 단독을 "Chicco" 인용으로 정당화) | **신규 blind spot** |
| **Influenza B Vic/Yam, HIV-1 group, SARS-CoV-2 Omicron lineage 분리** | None | **신규 blind spot** |
| **DURC 명목 + 한국 IBC** | None (cycle 3까지 P3CO 단편 추가) | **신규 blind spot** |
| **AlphaFold-Multimer (trimer SASA)** | None | **신규 blind spot** |
| **Sequence dedup tool 명시 (CD-HIT/MMseqs2)** | None | **신규 blind spot** |

**cycle 1~3은 "4-Phase paper-plan + 챕터별 codex IV&V"라는 동일한 framework를 3회 반복**했다. 그 framework는 (1) verbatim consistency, (2) statistical correctness within reported tests, (3) circularity audit, (4) caveat-grid completeness 4축이 강했다. 그러나 \textbf{licensing, query reproducibility, negative-result reporting, alternate distance-matrix tests, sub-lineage stratification, ethics-formal compliance, structural-tool citation breadth}는 한 번도 점검 frame에 들지 않았다.

이 8개 차원이 cycle 1~3의 공유 blind spot이며, 그 안에서 본 review가 신규 20건 (Critical 1 / Major 9 / Minor 10)을 발견했다.

---

## 종합 판정

- **신규 결함**: 20건 (Critical 1, Major 9, Minor 10)
- **defense 차단 위험**: **있음**

차단 위험의 근거:
1. **M1 (라이선스)** — Critical. ESM-2 weights non-commercial 약관과 본인 코드 "open-source license" 미명시는 reviewer 1명의 라이선스 질문 한 번에 무너진다. 24~48시간 내 라이선스 확정 필요.
2. **D1 (Influenza B Vic/Yam)** + **D3 (SARS-CoV-2 Omicron)** — 두 Major가 같이 묶이면 reviewer가 "best = freq for Influenza B"의 lineage-mixing artifact 우려와 "SARS-CoV-2 best = Tranception"의 시점 우려를 \textbf{동시에} 제기. 이 두 결함은 본문 내 1단락 sensitivity-mention만으로도 mitigation 가능 (full re-run은 불필요).
3. **S2 (F1/AUROC 병기)** — \texttt{stage3\_full\_results.csv}에 컬럼이 있을 가능성 매우 높으니 본문 1개 보충 표만 추가하면 즉시 닫힘.
4. **C1 (CD-HIT/MMseqs2)** — Methods reproducibility 정공법. 사용 tool명 1줄 추가만으로 닫힘.
5. **E1 (DURC)** — ch6:98에 "DURC" 명목 추가 + 한국 IBC 한 줄로 즉시 mitigation 가능.

**defense 92% 통과 확률 (cycle 3 평가)는 본 review 결함 중 위 5건을 patch하지 않을 경우 약 85%로 하락한다고 본다** (특히 M1 / D1+D3 two-Major-stack의 결합 위험이 가장 크다).

---

## 권장 대응 (priority)

| Priority | 결함 ID | 액션 | 시간 |
|----------|--------|-----|-----|
| P0 | M1 | LICENSE 파일 + 본문 ch3:1013에 license 명시 (예: "Apache 2.0; ESM-2 weights는 Meta non-commercial 약관 별도 적용") | 30분 |
| P0 | D1, D3 | ch5에 Influenza B Vic/Yam mixing + SARS-CoV-2 Omicron 시점 sensitivity 1단락씩 추가 (full re-run 면제, "limitation"으로 인정) | 1시간 |
| P0 | C1 | ch3:131에 dedup tool 1줄 명기 (예: "CD-HIT-EST v4.8.1 with 100% identity threshold") | 5분 |
| P1 | S2 | ch4 Table 8 (precision@k) 옆에 F1/AUROC 컬럼 1개 추가 | 30분 |
| P1 | E1 | ch6:98에 "DURC" + 한국 IBC framework 1줄 추가 | 5분 |
| P1 | M2 | ch3:131 옆에 가장 단순한 SARS-CoV-2 query 문자열 1개 본문 inline (나머지 10개는 CSV reference 유지) | 15분 |
| P2 | M3 | ch4 정규 표에 worst-end (음의 MCC) 카운트 1줄 추가 | 30분 |
| P2 | S1 | Mantel test 1회 (n=11 distance matrix, scipy/skbio로 5분 cost) 결과 ch4:528 단락에 1줄 | 30분 |
| P3 | 나머지 11건 (Minor) | Defense 후 patch 가능 | --- |

총 P0+P1+P2 P-time ≈ **4시간 이내**로 closing 가능.

---

본 review는 cycle 1~3 결함 list를 의도적으로 차단한 \textbf{외부 시각}이다. 같은 framework 3회 반복이 만들어낸 blind spot 8개 차원을 식별했고, 그 안에서 신규 20건을 발견했다. cycle 3 "92% defense pass"는 본 review의 P0/P1 patch (≈3시간) 후에야 안전한 추정이 된다.
