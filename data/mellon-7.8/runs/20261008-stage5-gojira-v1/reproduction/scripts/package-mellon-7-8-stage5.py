#!/usr/bin/env python3
"""Save runnable study sources, provenance, table schemas and output hashes."""
import argparse,csv,json,platform,shutil,subprocess
from pathlib import Path
from mellon_7_8_stage4 import dump,sha
ROOT=Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--site',type=Path,required=True);a=p.parse_args();run=a.work/'run';m=json.loads((run/'selection-manifest.json').read_text());target=a.site/'data/mellon-7.8/runs'/m['run_id'];target.mkdir(parents=True,exist_ok=True)
 assert json.loads((run/'cache-map-manifest.json').read_text())['schema']=='alpha60-paired-cache-portraits/1'
 assert json.loads((run/'validation-receipt.json').read_text())['status']=='passed'
 for path in run.iterdir():
  if path.is_file():shutil.copyfile(path,target/path.name)
 repro=target/'reproduction';(repro/'scripts').mkdir(parents=True,exist_ok=True)
 names=['check-mellon-7-8-stage5-browser.mjs','build-mellon-7-8-stage5.py','check-mellon-7-8-stage5.py','render-mellon-7-8-stage5.py','package-mellon-7-8-stage5-maps.py','package-mellon-7-8-stage5.py','build_mellon_stage5_import.py','mellon_7_8_stage4.py','analyze-mellon-7-8-stage4.py','render-mellon-7-6-aapi.py','mellon_7_6_native_maps.py','mellon-7-6-city-maps.cc','prepare-country-cartography.py','country_cartography.py','media_object_audit_figures.py','izzi_weekly_graphs.py','izzi-weekly-graphs.cc','izzi-weekly-graph-hover.js','mellon-7.8-stage5.js','mellon-7.8-stage5.css','compile-source.sh']
 for name in names:shutil.copyfile(ROOT/'scripts'/name,repro/'scripts'/name)
 (repro/'config/mellon-7.8/stage-5').mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'config/mellon-7.8/stage-5/release-context.json',repro/'config/mellon-7.8/stage-5/release-context.json')
 # Native build is based on the recorded alpha60 commit plus these exact edits.
 (repro/'src').mkdir(exist_ok=True)
 for name in ['a60-carto-geo.cc','a60-svg-cumulative-country.h']:shutil.copyfile(ROOT/'src'/name,repro/'src'/name)
 for name in ['paired-style.json','region-definition.json']:shutil.copyfile(a.work/name,target/name)
 readme='''# Reproduce this Gojira run

Use the annual repository revisions in `selection-manifest.json` and verify every selected input against `input-manifest.json`. The 2026 source is the latest upstream revision checked at freeze. Embedded GeoJSON version `20260701` is distinct from companion export version `2026-08-05`; the geolocation version is recorded by the companion products, not an embedded interval field.

From an alpha60 checkout with the recorded dependencies, overlay these `reproduction/scripts` and `reproduction/src` files. Keep a historical site checkout (or the preserved dated page) available for the city comparison and original ledger.

1. `python3 scripts/build-mellon-7-8-stage5.py --sources /path/to/pinned-checkouts --site /path/to/site --run /path/to/work/run`
2. `python3 scripts/check-mellon-7-8-stage5.py --sources /path/to/pinned-checkouts --run /path/to/work/run`
3. Build `a60-carto-geo.cc` with `scripts/compile-source.sh`. Obtain the original cache archives named in the two cache-input manifests; verify their hashes and extract only `*cumulative*.json`. Use the recorded torrent inventories, geolocation database and boundary file.
4. Render each film through `--cumulative-maps CACHE_DIR KEY --country JPN --region-definition region-definition.json --country-boundaries map-boundaries.json --country-iso-registry /path/to/slim-3.json --map-style paired-style.json`. Set `a60_PREFIX_DIR`, `a60_DATA_DIR` and `a60_GEOLOCATION_DB` to the pinned inputs. The executable writes beneath `tmp/` in its working directory. The saved style freezes the union frame and shared radius coefficient; do not rescale titles separately.
5. The map packaging helper expects `final-minus/tmp` and `final-empire/tmp`, extracted inputs under `cache-minus/cache.20241030` and `cache-empire/cache.20241111`, and the executable `a60-carto-geo-final.exe` beneath `--work`. It validates vector geometry, bubble-area conservation, shared frames and accounting before creating WebP previews and 3840-pixel images through Inkscape and ImageMagick.
6. Run `render-mellon-7-8-stage5.py --work /path/to/work --site /path/to/site`, then `package-mellon-7-8-stage5.py` with the same arguments. The existing Jekyll site supplies its theme and shared interaction assets. Build and run desktop/mobile checks before publication.

The Python reducer uses NumPy and Shapely; H3 uses the installed C library through ctypes. Native rendering uses GCC, Izzi, Cartofreako, RapidJSON, libtorrent, geolite2++, MaxMindDB and H3. Film cache maps and weekly comparisons span matching 26-week date windows with different aggregation grains. Shorter Monarch samples use available common weeks. Daily diagnostics retain their initial 105-day window. Weekly and daily interval grains are separate. No private IP cache documents are published.
'''
 (repro/'README.md').write_text(readme)
 tables=[]
 for path in target.glob('*.csv'):
  with path.open() as f:r=csv.reader(f);fields=next(r);count=sum(1 for _ in r)
  tables.append({'file':path.name,'rows':count,'fields':fields,'sha256':sha(path)})
 dump(target/'table-manifest.json',tables)
 receipt={'python':platform.python_version(),'alpha60_base_revision':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'native_compile':'scripts/compile-source.sh src/a60-carto-geo.cc a60-carto-geo-final.exe','software':{}}
 for command in [['g++','--version'],['inkscape','--version'],['magick','--version']]:receipt['software'][command[0]]=subprocess.check_output(command,text=True).splitlines()[0]
 dump(target/'build-receipt.json',receipt)
 artifacts={str(p.relative_to(a.site)):sha(p) for p in target.rglob('*') if p.is_file() and p.name!='artifact-manifest.json'}
 for p in (a.site/'resources').glob('mellon-7.8-stage5*'):artifacts[str(p.relative_to(a.site))]=sha(p)
 for p in (a.site/'_includes').glob('mellon-7.8-stage5*'):artifacts[str(p.relative_to(a.site))]=sha(p)
 for p in (a.site/'docs/figures').glob('godzilla*country*'):artifacts[str(p.relative_to(a.site))]=sha(p)
 for p in [a.site/'docs/godzilla.md',a.site/'docs/godzilla-20261008-historical.md',a.site/'data/mellon-7.8/stage5-current.json']:artifacts[str(p.relative_to(a.site))]=sha(p)
 dump(target/'artifact-manifest.json',{'run_id':m['run_id'],'artifacts':artifacts,'self_hash_excluded':True})
 print(json.dumps({'artifacts':len(artifacts),'tables':len(tables),'status':'packaged'}))
if __name__=='__main__':main()
