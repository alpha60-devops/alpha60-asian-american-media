"""Load the command-line stage 5 builder for shared pure helpers."""
import importlib.util
from pathlib import Path

def load_builder():
    spec=importlib.util.spec_from_file_location('gojira_builder',Path(__file__).with_name('build-mellon-7-8-stage5.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
