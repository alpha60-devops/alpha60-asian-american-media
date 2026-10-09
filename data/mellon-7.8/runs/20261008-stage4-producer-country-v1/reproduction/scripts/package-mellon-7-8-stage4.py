#!/usr/bin/env python3
"""Save code, runtime provenance and output hashes for the published study."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil

ROOT=Path(__file__).resolve().parents[1]
FILES=['mellon_7_8_stage4.py','analyze-mellon-7-8-stage4.py','render-mellon-7-8-stage4.py','check-mellon-7-8-stage4.py','test-mellon-7-8-stage4.py','package-mellon-7-8-stage4.py','mellon-7.8-stage4-map.html','mellon-7.8-stage4-map.js','izzi_weekly_graphs.py','izzi-weekly-graphs.cc','izzi-weekly-graph-hover.js']
README='''# Reproduce the producer-country study

Use the pinned revisions in `../input-manifest.json`. Metadata and annual result
repositories must be sibling checkouts. Do not fetch newer inputs implicitly.
From this reproduction directory, with Python, NumPy, Shapely, libh3 v4 and g++:

```sh
python3 scripts/mellon_7_8_stage4.py freeze --source-root /path/to/checkouts --out /tmp/reproduced-stage4
python3 scripts/mellon_7_8_stage4.py calculate --source-root /path/to/checkouts --out /tmp/reproduced-stage4
python3 scripts/analyze-mellon-7-8-stage4.py --run /tmp/reproduced-stage4
python3 scripts/check-mellon-7-8-stage4.py --run /tmp/reproduced-stage4 --source-root /path/to/checkouts
```

The analyzer and checker also accept the published `.json.gz` object ledgers.
Rendering needs the Izzi revision in `../figure-manifest.json` and an AAM checkout:

```sh
python3 scripts/render-mellon-7-8-stage4.py --run /tmp/reproduced-stage4 --site /tmp/aam-site --izzi /path/to/izzi --map-vendor /path/to/aam/resources/stage4-vendor --world /path/to/aam/resources/stage4-vendor/world.geojson
python3 scripts/package-mellon-7-8-stage4.py --site /tmp/aam-site
```

Run validation before rendering so its receipt is included. The artifact
manifest hashes public compressed objects, tables, figures, map assets and code.
Counts remain integers; interval definitions and the bootstrap seed are saved.
See environment.json for software versions and the libh3 binary hash. All title
and company country evidence remains in the selection and policy files.
'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--site',type=Path,required=True);a=p.parse_args();site=a.site
    pointer=json.loads((site/'data/mellon-7.8-stage4-current.json').read_text());run=site/'data/mellon-7.8/runs'/pointer['run_id'];rep=run/'reproduction'
    assert (run/'validation.json').exists()
    (rep/'scripts').mkdir(parents=True,exist_ok=True)
    for name in FILES:shutil.copyfile(ROOT/'scripts'/name,rep/'scripts'/name)
    policy=rep/'config/mellon-7.8/stage-4';policy.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(run/'producer-country-policy.json',policy/'producer-country-policy.json')
    (rep/'README.md').write_text(README)
    env={'python':platform.python_version(),'packages':{n:importlib.metadata.version(n) for n in ['numpy','shapely']},'h3_library_sha256':hashlib.sha256(Path('/lib64/libh3.so').read_bytes()).hexdigest(),'map_library':'Leaflet 1.9.4','map_outlines':'Natural Earth v5.1.2 ne_110m_admin_0_countries; public domain','outlines_url':'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_110m_admin_0_countries.geojson'}
    (rep/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    paths=[x for x in run.rglob('*') if x.is_file() and x.name!='artifact-manifest.json']
    paths+=list((site/'resources/stage4-vendor').glob('*'))
    paths+=[site/'resources'/n for n in ['mellon-7.8-stage4-map.html','mellon-7.8-stage4-map.js']]
    paths+=list((site/'resources').glob('mellon-7.8-stage4-*.svg'))
    paths += [site/'docs/asia-asian-where.md', site/'_includes/mellon-7.8-stage4-study.md',
              site/'data/mellon-7.8-stage4-current.json']
    manifest={'run_id':run.name,'artifacts':[{'path':str(x.relative_to(site)),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in sorted(paths)],'tables':[x.name for x in run.glob('*.csv')]}
    (run/'artifact-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(len(paths),'artifacts hashed')

if __name__=='__main__':main()
