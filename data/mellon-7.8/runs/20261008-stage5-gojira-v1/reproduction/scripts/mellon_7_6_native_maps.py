"""Compile native cartography and prepare topologically valid country outlines."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET


class NativeMaps:
    def __init__(self, site, cartofreako, izzi, countries, lakes):
        self.site = site
        self.temp = tempfile.TemporaryDirectory(prefix='alpha60-native-city-maps-')
        self.directory = Path(self.temp.name)
        root = Path(__file__).parent
        spec = importlib.util.spec_from_file_location('boundaries', root / 'prepare-country-cartography.py')
        prepare = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prepare)
        prepare.CODES = ['PHL', 'IND', 'AUS', 'JPN', 'KOR', 'CHN', 'USA']
        prepare.NAMES['AUS'] = 'Australia'
        self.boundaries = site / 'data/mellon-7.6-map-boundaries.json'
        prepare.prepare(countries, self.boundaries, lakes)
        header = cartofreako / 'src.projections/cart0freak0-cahill-keyes.h'
        (self.directory / 'ck-native.h').write_text(header.read_text().split('namespace a60::carto {', 1)[0] + '\n#endif\n')
        self.executable = self.directory / 'city-maps'
        subprocess.run(['g++', '-std=c++20', '-O2', '-I'+str(izzi/'src'), '-I'+str(self.directory),
                        str(root/'mellon-7-6-city-maps.cc'), '-o', str(self.executable)], check=True)
        commit = subprocess.check_output(['git', '-C', str(cartofreako), 'rev-parse', 'HEAD'], text=True).strip()
        self.provenance = {
            'url': f'https://github.com/bdekoz/cartofreako/blob/{commit}/src.projections/{header.name}',
            'sha256': hashlib.sha256(header.read_bytes()).hexdigest(),
            'izzi_commit': subprocess.check_output(['git', '-C', str(izzi), 'rev-parse', 'HEAD'], text=True).strip(),
            'boundary_sha256': hashlib.sha256(self.boundaries.read_bytes()).hexdigest(),
            'source': 'Natural Earth 1:10m countries minus 1:10m lakes, v5.1.2',
            'projection': 'Cartofreako native Cahill–Keyes; +1 degree registration; clipped seams; uniform fitting per country; Izzi SVG.',
            'renderer_sha256': hashlib.sha256((root/'mellon-7-6-city-maps.cc').read_bytes()).hexdigest(),
            'geometry_preparer_sha256': hashlib.sha256((root/'prepare-country-cartography.py').read_bytes()).hexdigest(),
        }

    def render(self, name, payload, executable=None, boundaries=None):
        source = self.directory / (name + '.json')
        source.write_text(json.dumps(payload, ensure_ascii=False))
        path = self.site / 'resources' / name
        subprocess.run([str(executable or self.executable), str(boundaries or self.boundaries), str(source), str(path)], check=True, stdout=subprocess.DEVNULL)
        path = self.site / 'resources' / (name + '.svg')
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        tree = ET.parse(path)
        root = tree.getroot()
        root.set('id', name)
        root.set('class', 'analysis-svg')
        root.set('role', 'group')
        root.set('aria-label', payload['title'] + '. ' + payload['subtitle'])
        if 'canvas_points' in payload:
            width, height = payload['canvas_points']
            root.set('width', f'{width}pt')
            root.set('height', f'{height}pt')
        for child in root:
            if child.tag.endswith('}title'): child.text = payload['title']
        tree.write(path, encoding='unicode')
        shutil.copyfile(path, self.site / '_includes' / path.name)
