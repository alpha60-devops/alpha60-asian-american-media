# Reproduce the producer-country study

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
