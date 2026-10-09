#!/usr/bin/env python3
"""Validate and package paired native cumulative-cache portraits."""
import argparse,json,subprocess,shutil
from pathlib import Path
from country_cartography import digest,compact_native_svg
from media_object_audit_figures import validate_country_map
from mellon_7_8_stage4 import dump

KEYS=['godzilla-minus-one','godzilla-x-kong-the-new-empire']

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--site',type=Path,required=True);p.add_argument('--style-only',action='store_true');a=p.parse_args();work=a.work
 if a.style_only:
  records=[];points={'JPN':set(),'asia-28':set()}
  for label,key in zip(['minus','empire'],KEYS):
   directory=work/('proof-'+label)/'tmp';acc=json.loads((directory/f'{key}-country-source-accounting.json').read_text())
   for code in points:
    records.append(json.loads((directory/f'{key}-data-country-{code.lower()}.json').read_text()))
    points[code].update(tuple(p) for p in acc['country_coordinates'][code])
  dump(work/'paired-style.json',{'radius_base':min(r['radius_base'] for r in records),'frame_points':{c:sorted(v) for c,v in points.items()},'display_minimum':0,'opacity':0.05,'frame_rule':'union of native boundary and both cache coordinate sets'})
  return
 out=a.site/'docs/figures';out.mkdir(parents=True,exist_ok=True);run=work/'run';assets={};records=[];validation=[];accounting=[]
 for label,key,date in zip(['minus','empire'],KEYS,['20241030','20241111']):
  directory=work/('final-'+label)/'tmp';accpath=directory/f'{key}-country-source-accounting.json';acc=json.loads(accpath.read_text());shutil.copyfile(accpath,out/accpath.name);assets[accpath.name]=digest(out/accpath.name)
  cache=work/('cache-'+label)/('cache.'+date)
  source={'key':key,'archive':{'path':f'/home/bkoz/src/alpha60-samples-cache/{key}.cache/cache.{date}.tar.xz'},'files':[{'path':p.name,'sha256':digest(p),'bytes':p.stat().st_size} for p in sorted(cache.glob('*cumulative*.json'))]}
  source['archive']['sha256']=digest(source['archive']['path'])
  source['torrent_inventory']=[{'path':p.name,'sha256':digest(p)} for p in sorted((Path('/home/bkoz/src/alpha60-data/torrent')/key).glob('*.torrent'))]
  for code in ['JPN','asia-28']:
   receipt=json.loads((directory/f'{key}-data-country-{code.lower()}.json').read_text());variant=next(v for v in receipt['variants'] if v['group']=='combined');assert variant['status']=='rendered'
   for role in ['downloaders','uploaders']:
    expected=sum(m['countries'][code][role] for m in acc['members'] if m['group']!='unsupported');assert expected==variant[role]
    world=sum(m[role] for m in acc['members']);unlocated=sum(m['unlocated'][role] for m in acc['members']);unsupported=sum(m['countries'][code][role] for m in acc['members'] if m['group']=='unsupported')
    assert world-unlocated-expected-unsupported>=0
    accounting.append({'key':key,'region':code,'role':role,'world':world,'selected_supported':expected,'selected_unsupported':unsupported,'unlocated_world':unlocated,'outside_region_located':world-unlocated-expected-unsupported})
   svg=out/variant['file'];compact_native_svg(directory/variant['file'],svg);validation.append(validate_country_map(svg,receipt,variant));assets[svg.name]=digest(svg)
   w,h=receipt['page']
   for edge,suffix in [(2112,''),(3840,'-4k')]:
    png=work/(svg.stem+suffix+'.png');webp=out/(svg.stem+suffix+'.webp')
    subprocess.run(['inkscape','--export-type=png','--export-width='+str(round(edge*w/max(w,h))),'--export-filename='+str(png),str(svg)],check=True)
    subprocess.run(['magick',str(png),'-quality','90',str(webp)],check=True)
    dimensions=subprocess.check_output(['magick','identify','-format','%w %h',str(webp)],text=True);assert max(map(int,dimensions.split()))==edge
    assets[webp.name]=digest(webp);png.unlink()
   receipt['receipt_file']=f'{key}-data-country-{code.lower()}.json';dump(out/receipt['receipt_file'],receipt);assets[receipt['receipt_file']]=digest(out/receipt['receipt_file']);records.append(receipt)
  source['member_inventory']=acc['members'];source['dates']=acc['dates'];dump(run/(key+'-cache-inputs.json'),source)
 # Shared frame, area scale and opacity must be identical between films.
 for code in ['JPN','asia-28']:
  rr=[r for r in records if r['country']==code];assert len(rr)==2
  assert len(rr[0]['panels'])==len(rr[1]['panels'])
  for field in ['page','radius_base','opacity']:assert rr[0][field]==rr[1][field],field
  for x,y in zip(rr[0]['panels'],rr[1]['panels']):
   for field in ['id','scale','translate','rect','bounds']:assert x[field]==y[field],(code,field)
 manifest={'schema':'alpha60-paired-cache-portraits/1','input_mode':'sample-cache-cumulative','records':records,'accounting':accounting,'validation':validation,'assets':assets,'style':json.loads((work/'paired-style.json').read_text()),'geolocation_database_sha256':digest('/home/bkoz/src/geoip-databases/ipinfo/standard_location.mmdb'),'renderer_sha256':digest(work/'a60-carto-geo-final.exe'),'boundary_sha256':digest(work/'boundaries.json'),'native_sources':{str(p):digest(p) for p in [Path('src/a60-carto-geo.cc'),Path('src/a60-svg-cumulative-country.h'),Path('src/a60-svg-collection.h')]},'revisions':{n:subprocess.check_output(['git','-C','/home/bkoz/src/'+n,'rev-parse','HEAD'],text=True).strip() for n in ['alpha60','izzi','cartofreako']}}
 dump(run/'cache-map-manifest.json',manifest);shutil.copyfile(work/'boundaries.json',run/'map-boundaries.json');dump(run/'cache-accounting.json',accounting)
 print('Four paired cache portraits validated',flush=True)
if __name__=='__main__':main()
