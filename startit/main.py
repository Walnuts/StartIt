import os
from jinja2 import Environment, Template

class Project(object):
    """
    so far I know you can use {{ project }} in the structure file,
    and the |lower filter.

    I plan on implementing/making sure the |title, |camel, and |upper
    filters work in the structure and specials files, and the |lower needs
    to work in the specials file.

    I also need to make sure {{ file }} can be used in the specials file.
    That probably means I'm gonna have to think about the order that everything
    is getting parsed in, because the filename isn't known till after the 
    yaml is parsed, but the yaml probably won't parse correctly until the 
    jinja parser is run...

    """

    def __init__(self, project_dir, project_title):
        self.project_dir = project_dir
        self.project_title = project_title

    def _proj_path(self, *args):
        return os.path.join(self.project_dir, *args)

    def parse_tree(self, coll, specials={}, collected_filename=""):
        if isinstance(coll, list):
            for part in coll:

                self.parse_tree(part,\
                        specials,\
                        collected_filename)

        elif isinstance(coll, dict):
            for k, v in coll.iteritems():
                fullpath = self._proj_path(collected_filename, k)
                print("Directory: %s\n" % (fullpath,))

                self.parse_tree(v,\
                        specials,\
                        os.path.join(collected_filename, k))

        else:
            if coll is not None:
                fullpath = self._proj_path(collected_filename, coll)
                if coll not in specials:
                    print("File: %s\n" % (fullpath,))
                else:
                    print("File: %s\n\tRule: %s" % (fullpath, specials[coll]))


def parse_file(yml, *args, **kwargs):
    def lower(mystr):
        title = ""
        for idx, char in enumerate(mystr):
            if idx != 0 and char.isupper():
                title = "{0}_{1}".format(title, char.lower())
            else:
                title = "{0}{1}".format(title, char.lower())
        return title

    env = Environment()
    env.filters['lower'] = lower
    struct_template = env.from_string(yml['structure'])
    specia_template = env.from_string(yml['specials'])
    
    return (
            yaml.load( struct_template.render(**kwargs) ),
            yaml.load( specia_template.render(**kwargs) )
            )
    

if __name__ == "__main__":
    import yaml
    from jinja2 import Template

    structure_file =\
    """
    - {{project}}:
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
            - {{project|lower}}_tests.py
        - __init__.py
        - main.py
        - controllers.py
        - models.py
        - settings.py
    """

    specials_file =\
    """
    jquery.js : |
        wget -O {{ file }} http://code.jquery.com/jquery-1.4.3.min.js
    reset.css : |
        wget -O {{ file }} http://meyerweb.com/eric/tools/css/reset/reset.css
    """

    project = "MyProject"
    cwd = "/Users/pwoolcoc/Python"

    
    st, sp = parse_file({"structure": structure_file,\
            "specials":specials_file}, project=project)

    myproj = Project(cwd, project)
    myproj.parse_tree(st, sp)


