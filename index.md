---
layout: default
title: "Asian American Media"
author: "Benjamin De Kosnik <bkoz@gnu.org>"
description: "Analysis of Asian American Media peer-to-peer distribution"
---


{::nomarkdown}
<img src="resources/a60-logo-block-gray.simple.svg?sanitize=true" height="50" width="100">

<div style="height: 50px;">
</div>
{:/}


## About

These are results from sampling peer swarms associated with *media objects*
being *shared* on the internet. Here, *media objects* are instances of media
that represent a specific film, television series or episode, or recorded
event as a file or archive. *Sharing* means the BitTorrent peer-to-peer file
sharing protocol. This is part of the long-term [Alpha60](https://alpha60.co/)
project.

## Asian American Media

Confirmed works in the expanded AAPI boundary with at least two qualifying
actor/primary-creator credits and USA Production: a confirmed U.S. production
company, commissioner, or platform, or existing confirmed U.S. production-country
evidence. The union includes reviewed
Asian diaspora and Native Hawaiian/Pacific Islander qualifications. The Asian
reference set is Asia-28, including Macau and Taiwan. No U.S.-citizenship minimum
applies. See the [set definition and current results](docs/aam.html).

Annual cohorts: 2017 to 2026. Observation dates vary by media object.

<div style="height: 50px;"></div>
{% include aam-media-objects-list.html %}
<div style="height: 50px;"></div>


## Results, Commentary
- [Asia-28 regional rankings](https://alpha60-devops.github.io/alpha60-results/docs/region-top-asia-28.html)
- [Asian American Media](docs/aam.html)
- [Asian American Media and Asian-global: geographic comparisons](docs/asia-asian-where.html)
- [The Pitt versus The Bear: India, Philippines and Australia](docs/pitt-bear-compare.html)
- [Godzilla and Monarch: Japan, USA, China and South Korea](docs/godzilla.html)
- [Fail: meta-compare aapi-led vs. white-led](https://github.com/bdekoz/alpha60/blob/main/docs/development/20260916_swarm_analysis_mellon_7.1_hex_space_cardinality_results.md)

<div style="height: 50px;"></div>


## Data

### Forms

The [Mellon 7.8 downloads](docs/aam.html#data-and-method) contain the current
recomputed group analysis. The files below are earlier published examples; the
expanded roster uses the annual sources pinned in the new selection manifest. The itemized links
above open annual sample-cache audits, which may describe newer exports or
different observation windows. Check the sample dates when comparing sources.

Each form links to an existing example from this group's `data/` directory.
Use the annual audit links above for measurements of newly included works.

- [Cumulative measurements (JSON)](data/3-body-problem-01-cumulative.json)
  - `<collection-key>-cumulative.json` — Collection totals and cumulative summaries.
- [Cumulative BTIH and media-object measurements (JSON)](data/3-body-problem-01-cumulative-btiha-media-objects.json)
  - `<collection-key>-cumulative-btiha-media-objects.json` — Torrent/media inventory and per-BTIH cumulative measurements.
- [Cumulative network classifications (JSON)](data/3-body-problem-01-cumulative-ip-swarm.json)
  - `<collection-key>-cumulative-ip-swarm.json` — IP-swarm and network summaries.
- [Weekly measurements (JSON)](data/3-body-problem-01-week.json)
  - `<collection-key>-week.json` — Weekly collection, BTIH, and country measurements.
- [Geographic observations (GeoJSON)](data/3-body-problem-01-cumulative.geojson)
  - `<collection-key>-cumulative.geojson` — Cumulative downloader and uploader geography.
- [Canonical media-object metadata (repository access required)](https://github.com/alpha60-devops/alpha60-swarm-metadata/tree/main/metadata)
  - `<collection-key>.json` — Descriptive source metadata.
- [JSON field documentation](docs/data-json.2026.html)

### [Source](https://github.com/alpha60-devops/alpha60-asian-american-media/tree/main/data)


{::nomarkdown}
<svg width="100" height=100>
    <circle cx="20" cy="50" r="10" fill="black"/>
</svg>
{:/}
