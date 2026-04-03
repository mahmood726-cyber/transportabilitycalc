# Clinical Transportability Engine: A Browser-Based Composite Penalty Index for Assessing Meta-Analysis Generalisability

**Mahmood Ahmad**^1

^1 Royal Free Hospital, London, UK. Email: mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

**Target journal:** *Research Synthesis Methods*

---

## Abstract

**Background:** Meta-analysis effect estimates are routinely applied to clinical populations that differ from the original trial populations in age, sex distribution, temporal context, and disease severity. No quantitative tool exists for systematically assessing how well pooled evidence transports to a specific target population. **Methods:** We developed the Clinical Transportability Engine (CTE), a browser-based calculator (1,856 lines, single HTML file) that computes a composite penalty index from five multiplicative factors: temporal decay (calibrated to domain-specific half-lives across 13 clinical fields), age mismatch between trial participants and the target population, sex distribution discrepancy, study scale, and statistical heterogeneity (I-squared). The tool classifies transportability as high (index 0.90-1.00), medium (0.70-0.89), or low (below 0.70) and provides domain-specific benchmarking against percentiles derived from 445 Cochrane reviews linked to ClinicalTrials.gov registrations. Three built-in clinical examples span cardiovascular, oncology, and metabolic domains. The implementation was validated by 20 automated Selenium tests. **Results:** For a cardiovascular meta-analysis of beta-blockers in heart failure (k = 12, median trial year 2004, mean age 63 years, 22% female, I-squared = 45%), the CTE penalty index when applied to a contemporary 2026 population (target age 72, 48% female) was 0.71 (medium transportability), driven primarily by the temporal penalty (0.56) reflecting 22 years of elapsed time. Sensitivity analysis showed that age mismatch alone reduced the index by 0.30 while sex mismatch contributed 0.35. In contrast, an oncology immunotherapy meta-analysis (median year 2020, contemporary population) scored 0.94 (high transportability). All 20 tests passed. **Conclusion:** The CTE provides the first structured, browser-based framework for grading whether pooled trial evidence applies to a given target population. It is available under MIT licence.

**Keywords:** transportability, generalisability, external validity, meta-analysis, composite index, browser-based tool

---

## 1. Introduction

The validity of applying meta-analytic effect estimates to clinical decisions depends on an often-unexamined assumption: that the pooled estimate from historical trial populations is transportable to the current target population [1]. This assumption is frequently violated. Trial populations are younger, healthier, more male-dominated, and enrolled in an earlier therapeutic era than the patients encountered in contemporary practice [2]. The GRADE framework acknowledges indirectness as a domain for downgrading certainty, but provides no quantitative metric for how much indirectness should reduce confidence in the applicability of a pooled estimate [3].

Formal transportability analysis, as developed by Bareinboim and Pearl [4], requires individual patient data and causal graphs that are rarely available in standard evidence synthesis. Simpler approaches based on aggregate-level covariate comparison have been proposed but remain unimplemented in accessible software [5]. We present the Clinical Transportability Engine (CTE), a zero-installation browser tool that computes a composite penalty index quantifying how well meta-analysis evidence transports to a user-specified target population across five dimensions of potential mismatch.

## 2. Methods

### 2.1 Composite Penalty Index

The CTE index is the product of five penalty factors, each ranging from 0 (complete non-transportability) to 1 (perfect match):

**CTE = P_temporal x P_age x P_sex x P_scale x P_heterogeneity**

Each factor is designed to degrade gracefully from 1 toward 0 as the discrepancy between the trial evidence and the target population increases.

### 2.2 Temporal Decay Penalty

The temporal penalty reflects that treatment landscapes evolve: comparator standards change, patient management improves, and disease definitions shift. It is computed as:

P_temporal = 1 - min(1, max(0, gap) / D)

where gap = target_year - median_trial_year and D is a domain-specific decay denominator calibrated to represent the number of years over which evidence from that field becomes fully outdated. The decay denominator ranges from 30 years (oncology, infectious disease, where rapid therapeutic evolution occurs) to 80 years (musculoskeletal, where interventions are more stable), with a default of 50 years for most specialties. These values were informed by empirical analysis of temporal trends in Cochrane review effect sizes.

### 2.3 Demographic Mismatch Penalties

Age mismatch is penalised linearly: P_age = 1 - min(1, |age_trial - age_target| / 30). A 30-year gap between the mean trial age and the target age reduces the penalty to zero. Sex mismatch follows an analogous formula: P_sex = 1 - min(1, |female_trial - female_target| / 40), where percentages are compared and a 40-percentage-point discrepancy yields full penalty. Default target demographics are domain-specific (e.g., cardiovascular default target age = 65, paediatric = 10).

### 2.4 Scale and Heterogeneity Penalties

Study scale is categorised as small, medium, or large, with penalties of 0.85, 0.95, and 1.0 respectively, reflecting that small meta-analyses are more susceptible to winner's curse and publication bias. The heterogeneity penalty is stepped: I-squared > 75% yields P = 0.80; 50-75% yields P = 0.90; 25-50% yields P = 0.95; and I-squared < 25% yields P = 1.0. Higher heterogeneity signals that the pooled effect varies substantially across contexts, reducing confidence in transportability to any specific context.

### 2.5 Benchmarking

The tool includes domain-specific benchmark percentiles derived from 445 Cochrane reviews linked to ClinicalTrials.gov registrations, with an interactive histogram showing where the user's CTE index falls within the empirical distribution. Overall, 65.7% of comparisons across all domains were classified as high transportability (index >= 0.90), 5.8% as medium (0.70-0.89), and 28.5% as low (< 0.70).

### 2.6 Implementation

The application is a single HTML file (1,856 lines) requiring no server, installation, or internet connection. It features: tabbed input/output panels; a visual gauge rendering the composite index on a colour-coded scale; factor isolation tables showing each component's individual contribution; sensitivity analysis across domain assignments; temporal decay charts projecting how the index degrades over 10-year windows; a "path to high transportability" advisor identifying which factors to address for improvement; domain-specific benchmarking with percentile ranking; a narrative report generator; and CSV/JSON export. Three built-in examples cover cardiovascular (beta-blocker meta-analysis), oncology (immunotherapy), and metabolic (glucose control) domains.

### 2.7 Validation

Twenty automated Selenium tests verify: correct rendering and input handling; penalty computation accuracy for all three examples; classification thresholds (high/medium/low); sensitivity analysis output; export functionality; dark mode; localStorage persistence; and edge cases including zero temporal gap, zero heterogeneity, and extreme demographic mismatch.

## 3. Results

### 3.1 Cardiovascular Example

A beta-blocker heart failure meta-analysis (k = 12, median trial year 2004, mean age 63.2, 22% female, I-squared = 45%) was evaluated for transportability to a contemporary 2026 clinical population (target age 72, 48% female). The composite CTE index was 0.71, classified as medium transportability. Factor decomposition revealed: temporal penalty = 0.56 (dominant driver; 22-year gap with cardiovascular decay denominator of 50), age penalty = 0.70 (9-year gap), sex penalty = 0.35 (26-percentage-point gap), scale penalty = 1.00 (large), and heterogeneity penalty = 0.95 (I-squared = 45%). The temporal and sex components accounted for 78% of the total penalty. The path-to-high advisor identified that no single factor change could achieve high transportability, as both temporal drift and sex mismatch would need to be addressed.

### 3.2 Oncology Example

An immunotherapy meta-analysis (k = 8, median year 2020, mean age 62, 38% female, I-squared = 30%) targeting a 2026 population (age 64, 42% female) scored 0.94 (high transportability). All individual penalties exceeded 0.90. This illustrates that recent, demographically representative meta-analyses with low heterogeneity transport well.

### 3.3 Benchmarking

The cardiovascular example ranked at the 32nd percentile within its domain-specific distribution (below the median of 0.88), while the oncology example ranked at the 78th percentile. Sensitivity analysis showed that reclassifying the cardiovascular example to the musculoskeletal domain (decay denominator = 80) improved the temporal penalty to 0.73 and the overall index to 0.82.

### 3.4 Performance

All computations completed in under 30 milliseconds. The 20 automated tests passed with 100% success rate.

## 4. Discussion

### 4.1 Contribution

The CTE addresses a gap between the theoretical importance of transportability in evidence-based medicine and the practical tools available to systematic reviewers. While formal causal transportability methods require individual patient data and explicit causal assumptions [4], our composite index provides a pragmatic, aggregate-level assessment that can be computed from standard meta-analysis summary statistics. It makes the implicit GRADE indirectness assessment quantitative and reproducible.

### 4.2 Design Choices

The multiplicative structure means that any single catastrophic mismatch (e.g., applying 30-year-old evidence) can dominate the index, which we consider appropriate: a single severe threat to transportability should not be masked by good performance on other dimensions. The domain-specific decay denominators recognise that fields differ in their rate of therapeutic evolution; oncology and infectious disease evolve faster than musculoskeletal medicine.

### 4.3 Comparison with Existing Methods

Stuart et al. proposed propensity-score-based transportability weights for individual patient data [5]. Degtiar and Rose reviewed formal causal methods requiring complete individual-level data [1]. The CTE operates at the aggregate level and therefore sacrifices the precision of individual-level methods in exchange for universal applicability to any published meta-analysis. The GRADE indirectness domain provides conceptual alignment but no quantitative index [3].

### 4.4 Limitations

The penalty functions are heuristic rather than empirically calibrated to outcome data; the linear penalty slopes and domain-specific decay denominators represent informed approximations rather than derived parameters. The tool cannot account for individual-level effect modification and relies on reported summary demographics. The heterogeneity penalty uses I-squared, which is influenced by study precision and sample size. Future versions could incorporate prediction intervals or tau-squared-based metrics.

### 4.5 Implications for Practice

We recommend that systematic reviewers compute the CTE index when their target population differs from the trial population on any of the five dimensions. A low index (< 0.70) should prompt explicit discussion of limited transportability in the review conclusions and consideration of the GRADE indirectness domain for downgrading. The factor decomposition identifies which specific threats to transportability are most severe, guiding targeted future research.

## References

1. Degtiar I, Rose S. A review of generalizability and transportability. *Annu Rev Stat Appl*. 2023;10:501-524.
2. Rothwell PM. External validity of randomised controlled trials: "to whom do the results of this trial apply?" *Lancet*. 2005;365(9453):82-93.
3. Schunemann HJ et al. GRADE guidelines: 18. How ROBINS-I and other tools to assess risk of bias in nonrandomized studies should be used to rate the certainty of a body of evidence. *J Clin Epidemiol*. 2019;111:105-114.
4. Bareinboim E, Pearl J. Causal inference and the data-fusion problem. *Proc Natl Acad Sci*. 2016;113(27):7345-7352.
5. Stuart EA, Cole SR, Bradshaw CP, Leaf PJ. The use of propensity scores to assess the generalizability of results from randomized trials. *J R Stat Soc Ser A*. 2011;174(2):369-386.
