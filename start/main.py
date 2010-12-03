import os
from pprint import pprint
import yaml

project_structure =\
"""
- ProjectDir:
    - static:
        - css:
            - reset.css
            - type.css
            - site.css
        - javascript:
            - jquery.js
            - application.js
        - images:
    - templates:
        - base.html
    - tests:
        - __init__.py
        - project_tests.py
    - __init__.py
    - main.py
    - controllers.py
    - models.py
    - settings.py
"""

specials =\
"""
jquery.js : |
    wget -O !$ http://code.jquery.com/jquery-1.4.3.min.js
reset.css : |
    wget -O !$ http://meyerweb.com/eric/tools/css/reset/reset.css
"""

def parse_tree(coll, collected_filename="", specials={}):
    if isinstance(coll, list):
        for part in coll:
            parse_tree(part, collected_filename, specials)
    elif isinstance(coll, dict):
        for k, v in coll.iteritems():
            print("Directory: %s" % (k,))
            parse_tree(v, os.path.join(collected_filename, k), specials)
    else:
        if coll is not None:
            fullpath = os.path.join(collected_filename, coll)
            if coll not in specials.keys():
                print("File: %s" % (fullpath,))
            else:
                print("File: %s\n\tRule: %s" % (fullpath, specials[coll]))

if __name__ == "__main__":
    struct = yaml.load(project_structure)
    special_cases = yaml.load(specials)
    parse_tree(struct, "", special_cases)
    #pprint(special_cases)


