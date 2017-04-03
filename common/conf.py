import os
from pyutil.program.jsonconf import parse

conf = parse(os.path.normpath(os.path.join(os.path.dirname(__file__), '../config/deploy.json')))
