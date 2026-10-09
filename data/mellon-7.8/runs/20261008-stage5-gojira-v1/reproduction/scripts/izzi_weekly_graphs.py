"""Native Izzi line charts; Python only assembles reviewed series and metadata."""
import hashlib
import json
import math
from copy import deepcopy
from pathlib import Path
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

COLORS = ['#175b8c','#9b4318','#606a24','#4d405d','#8c416d','#525252','#007f78']
DASHES = ['', '8 4', '2 4', '8 3 2 3', '9 4', '2 3', '']


def series(name, index, points):
    return {'name': name, 'color': COLORS[index], 'dash': DASHES[index], 'points': points}


def point(x, y, tooltip):
    return {'x': x, 'y': y, 'tooltip': tooltip}


class IzziWeeklyGraphs:
    def __init__(self, izzi, collection_keys=None):
        # Default for every caller: accepted native Izzi Disney+ plates.
        # https://alpha60-devops.github.io/alpha60-results-animation/docs/disney_plus.html
        # Native axes and direct 12pt media-object labels; WEEKS/DOWNLOADERS
        # for weekly downloader counts. Units for shares/calendar views stay explicit.
        self.collection_keys = collection_keys or {}
        self.temp = tempfile.TemporaryDirectory(prefix='alpha60-izzi-weekly-')
        self.directory = Path(self.temp.name)
        source = Path(__file__).with_name('izzi-weekly-graphs.cc')
        self.executable = self.directory/'weekly-graphs'
        subprocess.run(['g++','-std=c++20','-O2','-I'+str(izzi/'src'),str(source),'-o',str(self.executable)],check=True)
        self.provenance = {
            'library': 'Izzi',
            'default_layout': 'izzi-standard',
            'reference': 'https://alpha60-devops.github.io/alpha60-results-animation/docs/disney_plus.html',
            'interaction': 'izzi-weekly-graph-hover.js',
            'commit': subprocess.check_output(['git','-C',str(izzi),'rev-parse','HEAD'],text=True).strip(),
            'line_graph_header_sha256': hashlib.sha256((izzi/'src/izzi-svg-graphs-line.h').read_bytes()).hexdigest(),
            'renderer_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'interaction_sha256': hashlib.sha256(Path(__file__).with_name('izzi-weekly-graph-hover.js').read_bytes()).hexdigest(),
            'functions': ['svg::make_line_graph','svg::make_line_graph_annotations',
                          'svg::transform_to_graph_points','svg::make_marker_instance'],
        }
        self.specifications = {}

    def render(self, site, name, spec, inline=True):
        spec = deepcopy(spec)
        spec.setdefault('layout', 'izzi-standard')
        spec.setdefault('xlabel', 'WEEKS')
        if spec['layout'] == 'izzi-standard':
            spec['layout'] = 'izzi-standard'
            spec['columns'] = 1
            note = 'Media-object names appear directly on their lines; no separate legend.'
            if note not in spec['description']:
                spec['description'] += ' ' + note
            for panel in spec['panels']:
                panel.setdefault('ylabel', 'DOWNLOADERS')
                # Keep common comparison scales common, using native Izzi's
                # readable 1/2/5 tick ranges. The observations do not change.
                if 'y_max' in panel:
                    target = panel['y_max']
                    base = 10 ** math.floor(math.log10(target)) if target > 0 else 1
                    panel['y_max'] = next(base * n for n in [1, 2, 5, 10] if target <= base * n)
                for item in panel['series']:
                    key = self.collection_keys.get(item['name'], item['name'])
                    item['collection_key'] = key
                    # Use the table's display name for long keys so crowded
                    # country curves remain legible at the native 12pt size.
                    item['line_label'] = item['name'] if len(key) > 24 else key
        self.specifications[name] = spec
        source = self.directory/(name+'.json')
        source.write_text(json.dumps(spec,ensure_ascii=False))
        dest = site/'resources'/name
        subprocess.run([str(self.executable),str(source),str(dest)],check=True,stdout=subprocess.DEVNULL)
        path=site/'resources'/(name+'.svg')
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        tree=ET.parse(path);root=tree.getroot()
        if spec.get('layout') == 'izzi-standard':
            # Izzi supplies the tick positions and typography. Preserve the
            # approved calendar labels instead of displaying their bin indexes.
            calendar_ticks = {float(x): label for x, label in spec['ticks'] if label != str(x)}
            for group in root.iter():
                if group.get('id') == 'tic-x-labels':
                    for tick in group:
                        value = float(tick.text.strip())
                        if value in calendar_ticks:
                            tick.text = calendar_ticks[value]
        root.set('id',name);root.set('role','group');root.set('class','analysis-svg')
        root.set('aria-label',spec.get('accessible_title',spec['title'])+'. '+spec['description'])
        for el in root:
            if el.tag.endswith('}title'):el.text=spec['title']
        # Native markers already contain the exact value in a title. Expose
        # that same text to the page's focus/tap tooltip without changing marks.
        ns = '{http://www.w3.org/2000/svg}'
        for el in root.iter():
            if el.tag not in {ns+'circle', ns+'path', ns+'rect', ns+'polygon', ns+'g'}:
                continue
            title = el.find(ns+'title')
            if title is not None and title.text:
                tooltip = title.text.strip()
                el.set('data-tooltip', tooltip)
                el.set('tabindex', '0')
                el.set('role', 'img')
                el.set('aria-label', tooltip)
        ET.SubElement(root,'{http://www.w3.org/2000/svg}desc').text=spec['description']
        # Every chart can be safely embedded inline beside other charts.
        seen=set()
        for i,el in enumerate(root.iter()):
            if el is root:continue
            if el.get('id'):
                el.set('id',name+'-'+el.get('id')+'-'+str(i))
            if el.get('id'):assert el.get('id') not in seen;seen.add(el.get('id'))
        tree.write(path,encoding='unicode')
        if inline:shutil.copyfile(path,site/'_includes'/path.name)
        helper = Path(__file__).with_name('izzi-weekly-graph-hover.js')
        shutil.copyfile(helper, site/'resources'/helper.name)

    def save_ledger(self, path, merge=False):
        previous = json.loads(path.read_text()) if merge and path.exists() else {}
        charts = {**previous.get('charts', {}), **self.specifications}
        renderers = previous.get('chart_renderers', {name: previous.get('renderer') for name in previous.get('charts', {})})
        renderers.update({name: self.provenance for name in self.specifications})
        path.write_text(json.dumps({'renderer':self.provenance,'charts':charts,
                                   'chart_renderers':renderers},ensure_ascii=False,indent=2)+'\n')
