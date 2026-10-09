#!/usr/bin/env python3
"""Behavioral checks for producer/platform separation and missing H3 support."""
import importlib.util
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from mellon_7_8_stage4 import classify, empty, read_top

spec=importlib.util.spec_from_file_location('stage4_analysis',Path(__file__).with_name('analyze-mellon-7-8-stage4.py'))
analysis=importlib.util.module_from_spec(spec);spec.loader.exec_module(analysis)

class Stage4Tests(unittest.TestCase):
    def test_platform_does_not_change_producer_country(self):
        companies={'local studio':{'country_codes':['JPN']}}
        r={'production_tags':['local studio'],'distribution_tags':['netflix']}
        self.assertEqual(classify(r,companies)['group'],'non-usa-only')
        r['production_tags'].append('unresolved studio')
        self.assertEqual(classify(r,companies)['group'],'unknown')
        companies['unresolved studio']={'country_codes':['USA']}
        self.assertEqual(classify(r,companies)['group'],'mixed')
    def test_disputed_or_scoped_relationship_is_not_complete(self):
        r={'production_tags':['known'],'organization_relationships':[{'organization_id':'known','role':'production_company','review_status':'disputed'}]}
        self.assertEqual(classify(r,{'known':{'country_codes':['USA']}})['group'],'unknown')
    def test_country_divergence(self):
        self.assertAlmostEqual(analysis.js_divergence({'USA':1},{'USA':100}),0)
        self.assertAlmostEqual(analysis.js_divergence({'USA':1},{'JPN':1}),1)
        self.assertIsNone(analysis.js_divergence({}, {'USA':1}))
    def test_daily_groups_keep_unknown_homes_and_missing_days_unavailable(self):
        meta={k:{'canonical_work':k,'producer':{'group':g,'known_countries':['USA']},
                 'usa_production':{'qualification_basis':['platform:netflix']}}
              for k,g in [('known','usa-only'),('unknown','unknown'),('missing','usa-only')]}
        world=empty();world['downloaders']['size']=world['uploaders']['size']=100
        home=empty();home['downloaders']['size']=home['uploaders']['size']=25
        days=[{'index':i,'dates':str(i),'world':world,'countries':{'USA':home},
               'regions':{r:home for r in analysis.REGIONS},'sensitivity_eligible':i!=1} for i in [1,2,3]]
        data={k:{'days':days if k!='missing' else days[:2]} for k in meta}
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);receipt=analysis.daily_group_views(p,meta,data,3)
            self.assertEqual(receipt['complete_objects'],2)
            observations=list(csv.DictReader(io.StringIO((p/'daily-group-observations.csv').read_text())))
            self.assertTrue(all(r['share']=='' for r in observations if r['key']=='unknown' and r['region']=='producer-home'))
            rows=list(csv.DictReader(io.StringIO((p/'daily-group-summary.csv').read_text())))
            self.assertTrue(all(r['objects']=='1' for r in rows if r['kind']=='producer-group' and r['group']=='usa-only'))
            self.assertFalse(any(r['day']=='1' and r['coverage']=='audit-filtered' for r in rows))
    def test_missing_cells_are_null_but_observed_zeros_are_valid(self):
        h='85283473fffffff'
        def week(i,observed,n):
            v=empty();v['downloaders']['size']=n;v['uploaders']['size']=n
            world=empty();world['downloaders']['size']=world['uploaders']['size']=100
            return {'index':i,'world':world,'cells':{h:{'values':v,'countries':['USA']}} if observed else {}}
        class Geometry:
            def polygon(self,h):return {'type':'Polygon','coordinates':[[[0,0],[1,0],[1,1],[0,0]]]}
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            analysis.difference_map(p,'missing',[[week(1,True,10),week(2,True,10)]],[[week(1,True,0),week(2,False,0)]],[1,2],{},Geometry())
            f=json.loads((p/'missing.geojson').read_text())['features'][0]['properties']
            self.assertIsNone(f['downloaders_all_delta_pp'])
            self.assertEqual(f['downloaders_all_observed_common_delta_pp'],10)
            self.assertEqual(f['common_intervals'],1)
            analysis.difference_map(p,'zero',[[week(1,True,10)]],[[week(1,True,0)]],[1],{},Geometry())
            f=json.loads((p/'zero.geojson').read_text())['features'][0]['properties']
            self.assertEqual(f['downloaders_all_delta_pp'],10)

if __name__=='__main__':unittest.main()
