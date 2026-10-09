## Broader producer-country study

This study compares distribution geography by the countries of credited producers.
Platform and commissioner country remain separate AAM qualification evidence.
**Country coverage is limited:** the frozen population has 200 works, but the
reviewed company map resolves every listed producer tag for only 21. The other
179 remain unresolved; a U.S. platform does not resolve their producer country.
These are coverage-limited descriptions, not a census or a causal production effect.

### Population and coverage


| Producer-country group | Selected objects | Complete eight-week exports |
| --- | --- | --- |
| USA-only listed producers | 15 | 14 |
| Non-USA listed producers | 2 | 2 |
| Mixed listed producers | 4 | 4 |
| Unresolved producer country | 179 | 129 |

The population uses confirmed expanded AAPI membership and Threshold 2, with no
citizenship or USA Production filter. The producer grouping requires an exact
sourced country match for every production tag. “Complete” describes the listed
metadata credits; it does not certify all investors, service providers or financing.
Company headquarters identify the credited company's base, not filming locations
or its ultimate parent's nationality. Mixed producers remain a separate group.

The producer-country mapping and matching rules were frozen before the geographic
reduction. All 200 objects remain in the selection and exclusion ledgers. Of these,
149 have the first eight full weekly bins. The 51 shorter or missing windows are
reported rather than padded. Unknown producer groups are available in the downloads.
Beef and No More Bets retain their separate 15-week case comparison; neither has
complete producer-list mapping for the stricter cohort grouping.

[Selection, title evidence and company-country coverage](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/selection-manifest.json) · [Coverage and exclusion ledger](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/exclusions.csv) · [Frozen producer-country and matching rules](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/producer-country-policy.json)

### Regional trajectories

The boundaries are **Asia-28**, **EUR-27** and **USA–Canada**, using the existing
regional-ranking definitions. They do not overlap. Other classified and
unclassified geography remain in the worldwide denominator and downloads.
Each curve shows the region's share of that interval's worldwide role total.


{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.8-stage4-regional.svg %}
<figcaption>Weeks 1–15. Separate calendar years and film/season scopes remain limitations. Counts and hosting-excluded shares are downloadable. <a href="../resources/mellon-7.8-stage4-regional.svg">Download SVG</a>.</figcaption><div class="map-tooltip" role="status" aria-live="polite" hidden></div></figure>
{:/}

| Region | Role | Beef share (%) | No More Bets share (%) | Beef excluding hosting (%) | No More Bets excluding hosting (%) |
| --- | --- | --- | --- | --- | --- |
| Asia-28 | downloaders | 28.71 | 18.76 | 32.82 | 19.82 |
| EUR-27 | downloaders | 27.91 | 25.52 | 22.61 | 21.00 |
| USA–Canada | downloaders | 9.44 | 5.52 | 6.35 | 3.24 |
| Asia-28 | uploaders | 12.95 | 63.66 | 19.13 | 77.91 |
| EUR-27 | uploaders | 25.08 | 10.08 | 21.60 | 2.58 |
| USA–Canada | uploaders | 28.68 | 11.05 | 15.41 | 1.68 |

[All weekly regional weights and shares](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/weekly-regions.csv) · [Exact region code lists and source digest](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/region-definitions.json)

### Cohort distributions and matched comparisons

The following are unadjusted eight-week descriptions. Each sampled object receives
equal weight in the mean and median. The volume-weighted column uses observed
worldwide weights. Bootstrap intervals resample canonical works, keeping repeated
seasons or episode groups together; 1,000 replicates use a fixed saved seed.
Intervals describe variation in this selected, small sample, not uncertainty about
all media or unobserved peer locations.


| Group | Region | Objects / canonical works | Mean (%) | Median (%) | Middle 50% (%) | Mean bootstrap 95% interval | Volume-weighted (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| USA-only listed producers | Asia-28 | 14 / 11 | 26.22 | 25.97 | 22.32–28.69 | 23.80–29.30 | 26.92 |
| USA-only listed producers | EUR-27 | 14 / 11 | 16.23 | 16.18 | 13.19–17.26 | 13.77–18.02 | 15.94 |
| USA-only listed producers | USA–Canada | 14 / 11 | 13.29 | 9.39 | 8.59–17.76 | 8.71–16.41 | 13.06 |
| Non-USA listed producers | Asia-28 | 2 / 2 | 25.77 | 25.77 | 25.56–25.98 | 25.35–26.19 | 26.07 |
| Non-USA listed producers | EUR-27 | 2 / 2 | 11.32 | 11.32 | 10.78–11.86 | 10.24–12.40 | 10.54 |
| Non-USA listed producers | USA–Canada | 2 / 2 | 25.78 | 25.78 | 16.19–35.37 | 6.60–44.95 | 11.93 |
| Mixed listed producers | Asia-28 | 4 / 2 | 18.85 | 15.28 | 15.03–19.10 | 15.09–30.10 | 20.01 |
| Mixed listed producers | EUR-27 | 4 / 2 | 22.88 | 25.46 | 22.66–25.67 | 14.65–25.62 | 21.99 |
| Mixed listed producers | USA–Canada | 4 / 2 | 9.67 | 9.76 | 9.07–10.35 | 9.45–10.34 | 9.70 |

The Asian-global-only sensitivity, hosting-excluded results, uploader results
and audit-filtered summaries are included in the cohort download. Audit filtering
removes flagged opening bins and intervals overlapping recorded gaps; it does not
assert completeness for older audits that lack hourly gap detail. Remaining
sample years, genres, languages and episode/season scopes differ across groups.

Exact matching on sample year, object scope, language and genre family yields
**one stratum: Eternals / Fistful of Vengeance**, English-language action films
sampled in 2022. Their listed producers map to USA and Thailand. Both qualify
under the separate USA Production rule. Japan Sinks supplies the other non-USA
producer case (Japan), but has no eligible opposite-group match under these rules.
The matched stratum has one independent work on each side, so a population-level
confidence interval is unavailable. Missing genre/language evidence is not guessed.


| Matched region | Eternals share (%) | Fistful share (%) | Difference (percentage points) |
| --- | --- | --- | --- |
| Asia-28 | 32.91 | 26.19 | 6.72 |
| EUR-27 | 13.94 | 10.24 | 3.69 |
| USA–Canada | 7.62 | 6.60 | 1.02 |


The matched films' complete country distributions have Jensen–Shannon divergence **0.0528 bits** (0 means identical exported shares; 1 means disjoint support). This describes thresholded export distributions, not latent audiences.
[Cohort summaries and sensitivities](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/cohort-summary.csv) · [Per-work values](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/per-work.csv) · [Matched and unmatched strata](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/matching-manifest.json) · [Matched effects, coverage sensitivity and country distances](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/matched-comparisons.json)

<details markdown="1"><summary>Weekly cohort trajectories</summary>


{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.8-stage4-cohorts.svg %}
<figcaption>Fixed eight-week roster; equal-object weekly means. These unadjusted groups differ in year, genre and scope. <a href="../resources/mellon-7.8-stage4-cohorts.svg">Download SVG</a>.</figcaption><div class="map-tooltip" role="status" aria-live="polite" hidden></div></figure>
{:/}

</details>

### Producer and platform evidence

The evidence flags overlap: a work can have a U.S. producer and a U.S. platform.
The saved baseline country-or-producer flag is kept distinct from confirmed
company-country mappings. Fistful of Vengeance and Japan Sinks illustrate why
non-U.S. producer countries can coexist with USA Production qualification.
Beef and No More Bets keep their sourced producer examples and separate platform
review; no platform's country fills an unresolved production-company credit.

[Per-object evidence flags](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/evidence-branches.csv) · [Regional comparisons by evidence branch](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/evidence-branch-regions.csv)

### Daily share in the producer's home country

For Beef, the documented producer-country example is USA (A24); for No More Bets,
China (China Film Corporation). Daily shares divide exported home-country weights
by each day's exported worldwide weights. They use calendar dates in the source
files; the exports do not certify UTC, so no local-time or release-day alignment
is inferred. Home countries differ in scale and network coverage: these curves do
not estimate a home-country advantage.

Both objects have 105 daily exports in the chosen window. Raw observations and
seven-day trailing means are separate. The mean requires seven consecutive eligible
days; flagged boundary days and audit-gap dates leave gaps. No missing day is zero.
Daily sums differ from weekly totals in every tested role/week combination because
these products aggregate at different time grains. Daily curves therefore use daily
exports directly; weekly curves retain weekly exports.


{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.8-stage4-daily.svg %}
<figcaption>Days 1–105. First six rolling-window positions are unavailable; gap-affected and uncertified boundary-day windows are also unplotted. <a href="../resources/mellon-7.8-stage4-daily.svg">Download SVG</a>.</figcaption><div class="map-tooltip" role="status" aria-live="polite" hidden></div></figure>
{:/}
[Daily observations, coverage and seven-day means](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/daily-home-country.csv) · [Daily versus weekly grain diagnostic](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/daily-weekly-grain-check.csv)

### Daily producer and platform groups

The broader daily view uses the first 56 source calendar days. **107
objects have all 56 daily exports**; the remaining windows are listed in the
coverage ledger. Producer-home geography is the union of the countries of all
mapped listed producers. Mixed-country homes can cover several countries;
unresolved producer countries have no home-country value.

These are equal-object means on a fixed complete-export roster. The downloads
also contain daily medians, volume-weighted means, both roles, hosting exclusion,
and audit-filtered values. Audit filtering can change the daily denominator;
each row reports its object and canonical-work counts. Complete exports do not
certify complete hours within a day. Curves describe this selected sample.


| Mapped producer group | Complete 56-day objects |
| --- | --- |
| USA-only listed producers | 11 |
| Non-USA listed producers | 1 |
| Mixed listed producers | 1 |
| Unresolved producer country | 94 |

The non-USA daily group contains only Japan Sinks; the mixed daily group
contains only No Time to Die. These single-work curves do not estimate population
effects. Eternals is missing days 25, 26 and 27, and Fistful of Vengeance is missing
day 43, so neither enters the complete-window daily groups. Their weekly matched
comparison remains available; daily completeness is checked separately.

<details markdown="1"><summary>Daily shares in producer-home countries</summary>

{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.8-stage4-daily-groups.svg %}
<figcaption>First 56 days; fixed-roster means. Different home-country sizes and observation coverage limit comparisons. <a href="../resources/mellon-7.8-stage4-daily-groups.svg">Download SVG</a>.</figcaption><div class="map-tooltip" role="status" aria-live="polite" hidden></div></figure>
{:/}

</details>
<details markdown="1"><summary>Daily regional shares by producer/platform evidence</summary>

{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.8-stage4-daily-evidence.svg %}
<figcaption>Evidence branches overlap. All use the same named region and matching daily worldwide denominator. <a href="../resources/mellon-7.8-stage4-daily-evidence.svg">Download SVG</a>.</figcaption><div class="map-tooltip" role="status" aria-live="polite" hidden></div></figure>
{:/}

</details>
[Daily per-object observations](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/daily-group-observations.csv) · [Daily group summaries and sensitivities](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/daily-group-summary.csv) · [Daily window and country coverage](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/daily-group-coverage.csv)

### H3 resolution-5 differences and coverage

The maps compare **cell shares**, with positive values indicating a larger share
for the first work. They join exact H3 IDs at resolution 5 and the same elapsed
weekly index. The default difference is available only if both sides observe that
cell in every selected interval. A missing or suppressed cell is unavailable, not
zero. The coverage view shows those excluded cells explicitly.

Beef / No More Bets has only 62 cells observed on both sides in all 15 weeks;
Eternals / Fistful has 2,722 over eight weeks. Sparse common coverage limits what
the first map can show. World denominators still include weights outside the
common mask; the following table reports that coverage. Export and geolocation
versions agree within each mapped comparison. Country aggregation retains source
country codes; polygon centroids do not assign countries.


| Comparison | Side | Downloader weight retained in full mask (%) |
| --- | --- | --- |
| Beef / No More Bets | left | 35.11 |
| Beef / No More Bets | right | 42.32 |
| Eternals / Fistful | left | 91.88 |
| Eternals / Fistful | right | 95.84 |


{::nomarkdown}
<iframe src="../resources/mellon-7.8-stage4-map.html" title="Producer-country H3 differences and coverage" style="width:100%;height:920px;border:1px solid #aaa" loading="lazy"></iframe>
{:/}

[Open the interactive map](../resources/mellon-7.8-stage4-map.html). The map supports
role, hosting, coverage and regional views, with a keyboard-accessible cell table.

[Beef / No More Bets GeoJSON](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/beef-no-more-bets-h3.geojson) · [Beef / No More Bets coverage and exact differences](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/beef-no-more-bets-h3-coverage.csv)

[Eternals / Fistful GeoJSON](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/matched-stratum-1-h3.geojson) · [Eternals / Fistful coverage and exact differences](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/matched-stratum-1-h3-coverage.csv)

Resolution 8 is not needed for this comparison. The inputs are resolution 5 and
cannot supply finer within-cell locations. IP-geolocation accuracy and observation
density do not support a new resolution-8 claim here; no finer export was generated.

### Data, method and reproducibility

The measures are summed top-level aggregate GeoJSON swarm weights. Nested torrent
features are not added again. Addresses can recur across torrents and intervals;
these are not unique viewers or completed downloads. Hosting exclusion removes the
hosting flag from both numerator and denominator; it does not identify residential
users. Suppression and missing sampling hours remain coverage limits.

The run preserves the 197-work AAM roster and historical comparisons. All producer
classifications are analytical annotations with exact title/company sources. Source
commits and hashes, missing files, daily coverage, sampling windows, region lists,
matching, bootstrap settings and rendering specifications are downloadable.

- [Reproduction instructions and code](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/reproduction/README.md)
- [Input hashes and source revisions](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/input-manifest.json)
- [Analysis receipt](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/analysis-receipt.json)
- [Izzi figure specifications](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/figure-manifest.json)
- [Independent validation receipt](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/validation.json)
- [Output hashes and table manifest](../data/mellon-7.8/runs/20261008-stage4-producer-country-v1/artifact-manifest.json)

The scripts `mellon_7_8_stage4.py` (freeze and calculate), `analyze-mellon-7-8-stage4.py`, `render-mellon-7-8-stage4.py` and `check-mellon-7-8-stage4.py` reproduce this run from the pinned checkouts. Public per-object ledgers are compressed JSON in the run’s `objects/` directory.
