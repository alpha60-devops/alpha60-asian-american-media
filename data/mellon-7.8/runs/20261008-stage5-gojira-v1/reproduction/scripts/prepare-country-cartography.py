#!/usr/bin/env python3
"""Prepare pinned country land polygons, including lake shorelines, for native CK.

Shapely subtracts lake water and clips geographic polygon topology before the
C++ renderer projects it. No swarm data or projected coordinates are generated.
"""
import argparse
import hashlib
import json
from pathlib import Path

from shapely.geometry import shape, box
from shapely.ops import unary_union
from shapely.strtree import STRtree

SOURCE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_10m_admin_0_countries.geojson'
SOURCE_SHA = '239eec57ac17f100a11e2536cffc56752c318b50ae765b0918ff7aab4ce8f255'
LAKES_SOURCE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_10m_lakes.geojson'
LAKES_SHA = '2d036f53dedec578001c5c30c2959ee7d4eebc1306900fa4367c49929ec8f2d9'
CODES = ['PHL', 'IND', 'JPN', 'KOR', 'CHN', 'USA', 'AUS']
NAMES = dict(zip(CODES, ['Philippines', 'India', 'Japan', 'South Korea', 'China', 'United States', 'Australia']))
SEAMS = [-180, -111, -21, 69, 159, 180]


def read_pinned(path, expected):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f'upstream digest mismatch: {path}')
    return json.loads(raw)


def polygon_parts(geometry):
    if geometry.is_empty:
        return
    if geometry.geom_type == 'Polygon':
        yield geometry
    elif hasattr(geometry, 'geoms'):
        for child in geometry.geoms:
            yield from polygon_parts(child)


def remove_lake_water(country, lake_features, lake_geometries, tree):
    """Keep lake islands, and collect a country-specific water reference point."""
    water = []
    inventory = []
    for index in sorted(tree.query(country, predicate='intersects')):
        geometry = lake_geometries[index]
        if not geometry.is_valid:
            raise ValueError(f'invalid intersecting lake geometry: {lake_features[index]["properties"]["ne_id"]}')
        clipped = geometry.intersection(country)
        if clipped.area <= 1e-9:
            continue
        water.append(clipped)
        properties = lake_features[index]['properties']
        point = clipped.representative_point()
        inventory.append({'ne_id': properties['ne_id'],
                          'name': properties.get('name'),
                          'feature_class': properties['featurecla'],
                          'water_reference': [point.x, point.y]})
    land = country.difference(unary_union(water)) if water else country
    if not land.is_valid:
        raise ValueError('lake subtraction produced invalid land geometry')
    return land, inventory


def prepare(source, output, lakes):
    data = read_pinned(source, SOURCE_SHA)
    lake_features = read_pinned(lakes, LAKES_SHA)['features']
    lake_geometries = [shape(feature['geometry']) for feature in lake_features]
    tree = STRtree(lake_geometries)
    countries = []
    for code in CODES:
        features = [f for f in data['features'] if f['properties']['ADM0_A3'] == code]
        if len(features) != 1:
            raise ValueError(f'country mapping is not unique: {code}')
        feature = features[0]
        geom, lakes_used = remove_lake_water(shape(feature['geometry']), lake_features,
                                             lake_geometries, tree)
        polygons = []
        for west, east in zip(SEAMS, SEAMS[1:]):
            for part in polygon_parts(geom.intersection(box(west, -90, east, 90))):
                # One-sided projection at seam endpoints prevents cross-octant chords.
                rings = [[[min(east-1e-9,max(west+1e-9,x)),y] for x,y in ring.coords]
                         for ring in [part.exterior,*part.interiors]]
                polygons.append(rings)
        countries.append({'iso3':code, 'name':NAMES[code],
                          'mapping':{'field':'ADM0_A3','value':code,
                                     'source_ISO_A3':feature['properties']['ISO_A3']},
                          'lakes_removed':lakes_used,
                          'geometry':{'type':'MultiPolygon','coordinates':polygons}})
    result = {'schema':'alpha60-country-boundaries/1','source_url':SOURCE,
              'source_sha256':SOURCE_SHA,
              'source_version':'Natural Earth v5.1.2, 1:10m Admin-0 countries',
              'lakes_source_url':LAKES_SOURCE,'lakes_source_sha256':LAKES_SHA,
              'land_geometry':'admin-0 country minus intersecting 1:10m lakes and reservoirs',
              'license':'Natural Earth public domain','registration_longitude_degrees':1,
              'split_meridians':SEAMS,'countries':countries}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    print(output,output.stat().st_size)
    for country in countries:
        print(country['iso3'],len(country['lakes_removed']),'lake/reservoir features removed from land')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--lakes',type=Path,required=True,
                        help='pinned Natural Earth ne_10m_lakes.geojson')
    args = parser.parse_args()
    prepare(args.source,args.output,args.lakes)
